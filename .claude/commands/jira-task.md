# /jira-task — Create a Jira Task

Generate a complete, best-practice technical task and create it in Jira.
Tasks are used for engineering work that isn't a user-facing feature (e.g. infra, CI, migrations, refactors, spikes).

---

## Parameters (inferred from `$ARGUMENTS`)

| Param | Default | Override syntax |
|---|---|---|
| `--project` | `SCRUM` | Prefix with `KEY:` e.g. `MYPROJ: Set up CI` |
| `--priority` | `Medium` | Append `priority:High` |
| `--points` | inferred | Append `points:3` |
| `--labels` | inferred | Append `labels:infra,devops` |

---

## Task Generation Template

Generate ALL sections.

```
SUMMARY: <Clear action-oriented title, max 80 chars>

TASK DESCRIPTION
<2–3 sentences: what needs to be done, why, and what system/area it affects>

OBJECTIVE
<Single sentence: the specific, measurable outcome when this task is done>

BACKGROUND / MOTIVATION
<Why is this task needed now? What breaks or is at risk without it?>

DEFINITION OF DONE
- [ ] DOD1: <specific deliverable or state of the system>
- [ ] DOD2: <tests pass / coverage maintained>
- [ ] DOD3: <documentation updated if applicable>
- [ ] DOD4: <deployed to staging / reviewed by peer>
- [ ] DOD5: <no regressions in related areas>

IMPLEMENTATION NOTES
- <Specific files, services, or systems to touch>
- <Commands, tools, or scripts involved>
- <Config or environment changes needed>
- <Rollback plan if applicable>

DEPENDENCIES
- <Blocked by: any other ticket or external dependency>
- <Blocks: any downstream work waiting on this>

TESTING APPROACH
- <How to verify this task is complete>
- <Manual check steps or automated test to add>

STORY POINTS: <1|2|3|5|8>
PRIORITY: <High|Medium|Low>
LABELS: <label1,label2,...>
```

### Story point guide for tasks
| Points | Effort |
|--------|--------|
| 1 | Config change or trivial script, < 2 hours |
| 2 | Well-understood task, ~half day |
| 3 | Moderate task with some research, ~1 day |
| 5 | Complex task, multiple files/services, ~2–3 days |
| 8 | Large task or spike, ~1 week |

---

## API Call

```bash
cd /Users/rahultomar/rahul-dev/jira-story-generator && python3 create_jira_issue.py \
  --type Task \
  --project "<PROJECT>" \
  --summary "<summary>" \
  --description "<full task body>" \
  --points <n> \
  --priority "<High|Medium|Low>" \
  --labels "<label1,label2>"
```

---

## Examples
- `/jira-task Set up GitHub Actions CI pipeline`
- `/jira-task Migrate user table to UUID primary keys points:8 priority:High`
- `/jira-task MYPROJ: Write load tests for Payment API labels:performance,api`
