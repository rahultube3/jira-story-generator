# /jira-story — Create a Jira User Story

Generate a complete, best-practice user story from a plain summary and create it in Jira.

---

## Parameters (all inferred from `$ARGUMENTS` — no clarifying questions)

| Param | Default | Override syntax |
|---|---|---|
| `--project` | `SCRUM` | Prefix summary with `KEY:` e.g. `MYPROJ: Login API` |
| `--priority` | `High` | Append `priority:Medium` |
| `--points` | inferred | Append `points:5` |
| `--labels` | inferred | Append `labels:backend,api` |
| `--assignee` | unset | Append `assignee:<accountId>` |

---

## Story Generation Template

Generate ALL sections. Be specific — no placeholder text.

```
SUMMARY: <Verb - concise user-facing outcome, max 80 chars>

USER STORY
As a <specific role — not just "user">,
I want to <clear, atomic action>,
so that <measurable business or user benefit>.

BACKGROUND
<2–4 sentences: the problem being solved, why it matters now, what breaks without it>

ACCEPTANCE CRITERIA
Given <precondition>, when <trigger>, then <observable outcome>.

- [ ] AC1 (Happy Path): <core flow works end-to-end>
- [ ] AC2 (Happy Path): <secondary happy-path scenario>
- [ ] AC3 (Validation): <invalid input rejected with correct error>
- [ ] AC4 (Validation): <boundary value or missing field handled>
- [ ] AC5 (Error Handling): <downstream failure handled gracefully>
- [ ] AC6 (Edge Case): <duplicate action, self-referential, or limit exceeded>
- [ ] AC7 (Non-Functional): <performance, security, or accessibility requirement>
- [ ] AC8 (Side Effect): <audit log, notification, or event emitted>

OUT OF SCOPE
- <explicit exclusion 1>
- <explicit exclusion 2>

TECHNICAL NOTES
- Endpoint: METHOD /api/v1/<path>
- Request/response shape (key fields only)
- Auth requirement (JWT, API key, public)
- Dependencies or third-party services
- DB changes or migrations needed

STORY POINTS: <1|2|3|5|8|13>
PRIORITY: <High|Medium|Low>
LABELS: <label1,label2,...>
```

### Story point guide
| Points | Effort |
|--------|--------|
| 1–2 | Trivial, no unknowns, < 1 day |
| 3 | Small, understood, ~1–2 days |
| 5 | Moderate, some cross-cutting, ~3 days |
| 8 | Complex, multi-component, ~1 week |
| 13 | Large/uncertain — recommend splitting |

---

## API Call

```bash
cd /Users/rahultomar/rahul-dev/jira-story-generator && python3 create_jira_issue.py \
  --type Story \
  --project "<PROJECT>" \
  --summary "<summary>" \
  --description "<full story body>" \
  --points <n> \
  --priority "<High|Medium|Low>" \
  --labels "<label1,label2>" \
  --components "<component>" \
  --assignee "<accountId>"
```

Omit `--components` and `--assignee` if not applicable.

---

## Examples
- `/jira-story Login with Google OAuth`
- `/jira-story Card Payment API priority:High labels:payments,api`
- `/jira-story MYPROJ: User profile settings page points:3`
