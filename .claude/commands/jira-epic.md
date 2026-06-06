# /jira-epic — Create a Jira Epic

Generate a complete, best-practice Epic from a plain summary and create it in Jira.

---

## Parameters (inferred from `$ARGUMENTS`)

| Param | Default | Override syntax |
|---|---|---|
| `--project` | `SCRUM` | Prefix with `KEY:` e.g. `MYPROJ: Payments Platform` |
| `--priority` | `High` | Append `priority:Medium` |
| `--labels` | inferred | Append `labels:payments,backend` |

---

## Epic Generation Template

An Epic groups related stories under a single business goal. Generate ALL sections.

```
EPIC NAME: <short board-display name, max 60 chars — this appears on Jira boards>
SUMMARY: <full epic title, max 80 chars>

EPIC GOAL
<1–2 sentences: the single, clear business outcome this epic delivers>

BUSINESS VALUE
- <value point 1: revenue, retention, compliance, risk reduction, etc.>
- <value point 2>
- <value point 3>

PROBLEM STATEMENT
<2–3 sentences: what is broken or missing today, who is impacted, what the cost is>

SCOPE — IN
List the high-level capabilities this epic covers:
- <capability 1>
- <capability 2>
- <capability 3>
- <capability 4>

SCOPE — OUT
- <explicit exclusion 1 — with reason if useful>
- <exclusion 2>

CHILD STORIES (suggested breakdown)
- [ ] Story: <story 1 title> (~<n> pts)
- [ ] Story: <story 2 title> (~<n> pts)
- [ ] Story: <story 3 title> (~<n> pts)
- [ ] Story: <story 4 title> (~<n> pts)
- [ ] Story: <story 5 title> (~<n> pts)

DEPENDENCIES
- <upstream dependency: team or system that must deliver something first>
- <downstream impact: teams or features that depend on this epic>

SUCCESS METRICS
- <measurable KPI 1, e.g. "Payment success rate > 99.5%">
- <measurable KPI 2>

TECHNICAL NOTES
- High-level architecture or system design considerations
- Key integrations or third-party services
- Data, security, or compliance considerations

PRIORITY: <High|Medium|Low>
LABELS: <label1,label2,...>
```

### Priority guide for epics
| Priority | Meaning |
|----------|---------|
| High | Core product pillar, revenue-critical, or compliance-required |
| Medium | Important roadmap item, significant user impact |
| Low | Backlog, exploratory, or future phase |

---

## API Call

```bash
cd /Users/rahultomar/rahul-dev/jira-story-generator && python3 create_jira_issue.py \
  --type Epic \
  --project "<PROJECT>" \
  --summary "<summary>" \
  --epic-name "<short epic name>" \
  --description "<full epic body>" \
  --priority "<High|Medium|Low>" \
  --labels "<label1,label2>"
```

---

## Examples
- `/jira-epic Payments Platform`
- `/jira-epic User Authentication & Security labels:auth,security`
- `/jira-epic MYPROJ: Mobile App v2 priority:High`
