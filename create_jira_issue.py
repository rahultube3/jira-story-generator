#!/usr/bin/env python3
"""Unified CLI: create any Jira issue type (Epic, Story, Bug, Task, Subtask)."""

import argparse
import json
import sys
from base64 import b64encode
from pathlib import Path
from urllib import request, error


# ── env ───────────────────────────────────────────────────────────────────────

def load_env(env_path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        env[key.strip()] = value.strip()
    return env


# ── ADF ───────────────────────────────────────────────────────────────────────

def text_to_adf(text: str) -> dict:
    """Convert plain text (with blank-line paragraph breaks) to ADF."""
    content = []
    for block in text.strip().split("\n\n"):
        lines = block.splitlines()
        inline: list[dict] = []
        for i, line in enumerate(lines):
            if i > 0:
                inline.append({"type": "hardBreak"})
            inline.append({"type": "text", "text": line})
        if inline:
            content.append({"type": "paragraph", "content": inline})
    if not content:
        content.append({"type": "paragraph", "content": [{"type": "text", "text": text}]})
    return {"type": "doc", "version": 1, "content": content}


# ── constants ─────────────────────────────────────────────────────────────────

PRIORITY_MAP = {
    "highest": "Highest", "critical": "Highest",
    "high":    "High",
    "medium":  "Medium",  "med": "Medium",
    "low":     "Low",
    "lowest":  "Lowest",  "trivial": "Lowest",
}

VALID_ISSUE_TYPES = {"Epic", "Story", "Bug", "Task", "Subtask", "Feature", "Request"}


# ── main ──────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Create a Jira issue (Epic / Story / Bug / Task)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Story
  python3 create_jira_issue.py --type Story --project SCRUM \\
      --summary "Login API" --description "..." --points 5 --priority High

  # Epic
  python3 create_jira_issue.py --type Epic --project SCRUM \\
      --summary "Payments Platform" --epic-name "Payments Platform" --description "..."

  # Bug
  python3 create_jira_issue.py --type Bug --project SCRUM \\
      --summary "Checkout crashes on empty cart" --description "..." \\
      --priority High --severity Critical --environment "Chrome 124 / macOS"

  # Task
  python3 create_jira_issue.py --type Task --project SCRUM \\
      --summary "Set up CI pipeline" --description "..." --points 2
        """,
    )

    # ── required ──────────────────────────────────────────────────────────────
    p.add_argument("--summary",     required=True,  help="Issue title (max 255 chars)")
    p.add_argument("--description", required=True,  help="Full issue body (plain text)")
    p.add_argument("--project",     required=True,  help="Jira project key, e.g. SCRUM")

    # ── issue type ────────────────────────────────────────────────────────────
    p.add_argument("--type",        default="Story",
                   choices=sorted(VALID_ISSUE_TYPES),
                   help="Issue type (default: Story)")

    # ── common optional ───────────────────────────────────────────────────────
    p.add_argument("--priority",    default="Medium",
                   help="Highest|High|Medium|Low|Lowest (default: Medium)")
    p.add_argument("--labels",      default="",
                   help="Comma-separated labels, e.g. backend,api,auth")
    p.add_argument("--components",  default="",
                   help="Comma-separated component names")
    p.add_argument("--assignee",    default="",
                   help="Assignee account ID (Jira account ID, not email)")

    # ── story / task ──────────────────────────────────────────────────────────
    p.add_argument("--points",      type=float, default=None,
                   help="Story points — Fibonacci: 1 2 3 5 8 13")

    # ── epic ──────────────────────────────────────────────────────────────────
    p.add_argument("--epic-name",   default="",
                   help="(Epic only) Short epic name shown in board headers")

    # ── bug ───────────────────────────────────────────────────────────────────
    p.add_argument("--severity",    default="",
                   help="(Bug only) Critical|Major|Minor|Trivial")
    p.add_argument("--environment", default="",
                   help="(Bug only) Browser / OS / version where bug occurs")

    return p


def main() -> None:
    parser = build_parser()
    args   = parser.parse_args()

    # ── load credentials ──────────────────────────────────────────────────────
    env_file = Path(__file__).parent / ".env"
    if not env_file.exists():
        sys.exit(f"ERROR: .env not found at {env_file}")

    env      = load_env(env_file)
    api_url  = env.get("JIRA_CREATE_API", "").rstrip("/")
    username = env.get("USER_NAME", "")
    token    = env.get("API_TOKEN", "")

    if not all([api_url, username, token]):
        sys.exit("ERROR: .env must define JIRA_CREATE_API, USER_NAME, and API_TOKEN")

    credentials = b64encode(f"{username}:{token}".encode()).decode()

    # ── build fields ──────────────────────────────────────────────────────────
    priority_name = PRIORITY_MAP.get(args.priority.lower(), args.priority)
    labels        = [l.strip() for l in args.labels.split(",")     if l.strip()]
    components    = [{"name": c.strip()} for c in args.components.split(",") if c.strip()]

    fields: dict = {
        "project":     {"key": args.project},
        "summary":     args.summary,
        "description": text_to_adf(args.description),
        "issuetype":   {"name": args.type},
        "priority":    {"name": priority_name},
    }

    if labels:
        fields["labels"] = labels

    if components:
        fields["components"] = components

    if args.assignee:
        fields["assignee"] = {"accountId": args.assignee}

    # story points (customfield_10016 is the standard Jira field)
    if args.points is not None:
        fields["customfield_10016"] = args.points

    # epic-specific
    if args.type == "Epic" and args.epic_name:
        fields["customfield_10011"] = args.epic_name  # Epic Name field

    # bug-specific: append environment + severity to description body
    if args.type == "Bug":
        extra_lines: list[str] = []
        if args.environment:
            extra_lines.append(f"ENVIRONMENT: {args.environment}")
        if args.severity:
            extra_lines.append(f"SEVERITY: {args.severity}")
        if extra_lines:
            extra_block = "\n".join(extra_lines)
            full_text   = args.description.strip() + "\n\n" + extra_block
            fields["description"] = text_to_adf(full_text)
        if args.environment:
            fields["environment"] = text_to_adf(args.environment)

    # ── API call ──────────────────────────────────────────────────────────────
    payload = {"fields": fields}
    req = request.Request(
        api_url,
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type":  "application/json",
            "Accept":        "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(req) as resp:
            body = json.loads(resp.read())
    except error.HTTPError as exc:
        detail = exc.read().decode()
        sys.exit(f"Jira API error {exc.code}: {detail}")

    key  = body.get("key", "?")
    base = api_url.split("/rest/")[0]
    print(f"Created: {key}")
    print(f"Type:    {args.type}")
    print(f"URL:     {base}/browse/{key}")


if __name__ == "__main__":
    main()
