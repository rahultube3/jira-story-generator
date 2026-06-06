#!/usr/bin/env python3
"""CLI helper: create a Jira issue via the REST API v3."""

import argparse
import json
import sys
from base64 import b64encode
from pathlib import Path
from urllib import request, error


def load_env(env_path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        env[key.strip()] = value.strip()
    return env


def description_to_adf(text: str) -> dict:
    """Convert plain text to Atlassian Document Format."""
    content = []
    for paragraph in text.split("\n\n"):
        lines = paragraph.splitlines()
        inline: list[dict] = []
        for i, line in enumerate(lines):
            if i > 0:
                inline.append({"type": "hardBreak"})
            if line.startswith("- [ ] ") or line.startswith("- "):
                # render as bullet list item
                pass
            inline.append({"type": "text", "text": line})
        if inline:
            content.append({"type": "paragraph", "content": inline})

    if not content:
        content.append({"type": "paragraph", "content": [{"type": "text", "text": text}]})

    return {"type": "doc", "version": 1, "content": content}


PRIORITY_MAP = {
    "highest": "Highest",
    "high":    "High",
    "medium":  "Medium",
    "low":     "Low",
    "lowest":  "Lowest",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a Jira issue")
    parser.add_argument("--summary",      required=True)
    parser.add_argument("--description",  required=True)
    parser.add_argument("--project",      required=True, help="Jira project key, e.g. SCRUM")
    parser.add_argument("--issue-type",   default="Story")
    parser.add_argument("--story-points", type=float, default=None, help="Fibonacci: 1,2,3,5,8,13")
    parser.add_argument("--priority",     default="Medium", help="Highest|High|Medium|Low|Lowest")
    parser.add_argument("--labels",       default="", help="Comma-separated labels")
    args = parser.parse_args()

    env_file = Path(__file__).parent / ".env"
    if not env_file.exists():
        sys.exit(f"ERROR: .env not found at {env_file}")

    env = load_env(env_file)
    api_url  = env.get("JIRA_CREATE_API", "").rstrip("/")
    username = env.get("USER_NAME", "")
    token    = env.get("API_TOKEN", "")

    if not all([api_url, username, token]):
        sys.exit("ERROR: .env must define JIRA_CREATE_API, USER_NAME, and API_TOKEN")

    credentials = b64encode(f"{username}:{token}".encode()).decode()

    priority_name = PRIORITY_MAP.get(args.priority.lower(), args.priority)
    labels = [l.strip() for l in args.labels.split(",") if l.strip()]

    fields: dict = {
        "project":     {"key": args.project},
        "summary":     args.summary,
        "description": description_to_adf(args.description),
        "issuetype":   {"name": args.issue_type},
        "priority":    {"name": priority_name},
    }

    if labels:
        fields["labels"] = labels

    # customfield_10016 is the standard Jira story points field
    if args.story_points is not None:
        fields["customfield_10016"] = args.story_points

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
    print(f"URL: {base}/browse/{key}")


if __name__ == "__main__":
    main()
