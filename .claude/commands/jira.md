# /jira — Jira Issue Router

Detect the issue type from `$ARGUMENTS` and route to the correct generator. No clarifying questions — infer everything.

---

## Routing Rules

Read `$ARGUMENTS` and apply the first matching rule:

| If `$ARGUMENTS` contains… | Route to |
|---|---|
| `epic:` prefix OR words like "platform", "initiative", "phase", "programme" | **Epic** — follow `/jira-epic` template |
| `bug:` prefix OR "bug", "crash", "broken", "fails", "error", "regression", "not working" | **Bug** — follow `/jira-bug` template |
| `task:` prefix OR "set up", "migrate", "refactor", "spike", "configure", "deploy", "script", "ci", "infra" | **Task** — follow `/jira-task` template |
| anything else | **Story** — follow `/jira-story` template |

---

## Parameter Overrides (apply to all types)

Append any of these inline to `$ARGUMENTS`:

| Override | Example |
|---|---|
| Project key | `MYPROJ: <summary>` |
| Priority | `priority:High` |
| Story points | `points:5` |
| Labels | `labels:backend,api` |
| Assignee | `assignee:<accountId>` |
| Severity (bug) | `severity:Critical` |
| Environment (bug) | `env:"Chrome 124 / macOS"` |
| Epic name (epic) | `epicname:"Payments Platform"` |

---

## What to generate (by type)

### Story
Follow the full `/jira-story` template:
Summary · User Story (As a / I want / So that) · Background · Acceptance Criteria (min 6, typed: Happy Path / Validation / Error / Edge Case / Non-Functional / Side Effect) · Out of Scope · Technical Notes · Points · Priority · Labels

### Epic
Follow the full `/jira-epic` template:
Epic Name · Summary · Goal · Business Value · Problem Statement · Scope In/Out · Child Stories breakdown · Dependencies · Success Metrics · Technical Notes · Priority · Labels

### Bug
Follow the full `/jira-bug` template:
Summary · Description · Steps to Reproduce · Expected vs Actual · Environment · Severity · Frequency · Impact · Logs/Evidence · Root Cause Hypothesis · AC for Fix · Priority · Labels

### Task
Follow the full `/jira-task` template:
Summary · Description · Objective · Background · Definition of Done · Implementation Notes · Dependencies · Testing Approach · Points · Priority · Labels

---

## API Call (after generating and showing the issue to the user)

```bash
cd /Users/rahultomar/rahul-dev/jira-story-generator && python3 create_jira_issue.py \
  --type <Epic|Story|Bug|Task> \
  --project "<PROJECT>" \
  --summary "<summary>" \
  --description "<full body>" \
  [--epic-name "<name>"]       # Epic only
  [--points <n>]               # Story / Task
  [--severity "<severity>"]    # Bug only
  [--environment "<env>"]      # Bug only
  --priority "<priority>" \
  --labels "<label1,label2>"
```

Then report the issue key and URL.

---

## Quick Examples

```
/jira Login with Google OAuth                          → Story
/jira bug: Checkout crashes on empty cart              → Bug
/jira epic: Payments Platform                          → Epic
/jira task: Set up GitHub Actions CI pipeline          → Task
/jira P2P payment request feature priority:High        → Story
/jira bug: Safari login broken severity:Major          → Bug
/jira MYPROJ: Migrate DB to UUID keys points:8        → Task
```
