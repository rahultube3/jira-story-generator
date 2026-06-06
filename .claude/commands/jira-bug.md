# /jira-bug — Create a Jira Bug Report

Generate a complete, best-practice bug report from a plain description and create it in Jira.

---

## Parameters (inferred from `$ARGUMENTS`)

| Param | Default | Override syntax |
|---|---|---|
| `--project` | `SCRUM` | Prefix with `KEY:` e.g. `MYPROJ: Checkout crashes` |
| `--priority` | inferred from severity | Append `priority:High` |
| `--severity` | inferred | Append `severity:Critical` |
| `--environment` | inferred | Append `env:"Chrome 124 / macOS 14"` |
| `--labels` | inferred | Append `labels:frontend,checkout` |

### Severity → Priority mapping
| Severity | Priority |
|----------|----------|
| Critical (data loss, security, system down) | Highest |
| Major (core feature broken, no workaround) | High |
| Minor (feature degraded, workaround exists) | Medium |
| Trivial (cosmetic, typo, minor UI) | Low |

---

## Bug Report Generation Template

Generate ALL sections. Be precise — vague bugs never get fixed.

```
SUMMARY: <[BUG] Component - Concise symptom description, max 80 chars>

BUG DESCRIPTION
<2–3 sentences: what is broken, what the user experiences, why it matters>

STEPS TO REPRODUCE
1. <Exact step 1 — include URL, user state, data used>
2. <Exact step 2>
3. <Exact step 3>
4. <...>

EXPECTED BEHAVIOUR
<What should happen — be specific>

ACTUAL BEHAVIOUR
<What actually happens — error message, incorrect output, crash, etc.>

ENVIRONMENT
- Browser / App version: <e.g. Chrome 124.0.6367.82>
- OS: <e.g. macOS 14.4, iOS 17.4, Windows 11>
- Device: <e.g. iPhone 15 Pro, MacBook M3>
- User role / account state: <e.g. logged-in admin, guest, user with empty cart>
- API version / backend env: <e.g. staging, production, v2.3.1>

SEVERITY: <Critical|Major|Minor|Trivial>
FREQUENCY: <Always|Often (>50%)|Sometimes (<50%)|Rarely>

IMPACT
- <Who is affected: e.g. all users, mobile-only, users with X condition>
- <Business impact: e.g. blocks checkout, causes revenue loss, data corruption risk>

LOGS / EVIDENCE
- <Error message or stack trace snippet if known>
- <API response / status code if applicable>
- <Screenshot or recording note if available>

ROOT CAUSE HYPOTHESIS (if known)
<Optional: likely cause based on error messages or code knowledge>

ACCEPTANCE CRITERIA FOR FIX
- [ ] AC1: Steps to reproduce no longer produce the bug
- [ ] AC2: Expected behaviour is observed consistently across environments
- [ ] AC3: No regression in related functionality
- [ ] AC4: Unit/integration test added to prevent recurrence

PRIORITY: <Highest|High|Medium|Low>
LABELS: <label1,label2,...>
```

---

## API Call

```bash
cd /Users/rahultomar/rahul-dev/jira-story-generator && python3 create_jira_issue.py \
  --type Bug \
  --project "<PROJECT>" \
  --summary "<[BUG] summary>" \
  --description "<full bug report body>" \
  --priority "<Highest|High|Medium|Low>" \
  --severity "<Critical|Major|Minor|Trivial>" \
  --environment "<browser / OS / version>" \
  --labels "<label1,label2>"
```

---

## Examples
- `/jira-bug Checkout crashes when cart has more than 10 items`
- `/jira-bug Login fails on Safari iOS severity:Major env:"Safari 17 / iOS 17"`
- `/jira-bug MYPROJ: Payment confirmation email not sent priority:High`
