# jira-story-generator

Generate and create Jira issues (Epics, Stories, Bugs, Tasks) from the command line using the Jira REST API.

## Setup

1. Clone the repo
2. Copy `.env.example` to `.env` and fill in your credentials:
   ```bash
   cp .env.example .env
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables

| Variable | Description |
|---|---|
| `JIRA_CREATE_API` | Jira REST API endpoint for issue creation |
| `USER_NAME` | Your Atlassian account email |
| `API_TOKEN` | Your Jira API token ([generate here](https://id.atlassian.com/manage-profile/security/api-tokens)) |

## Usage

```bash
python3 create_jira_issue.py \
  --type Story \
  --project SCRUM \
  --summary "As a user, I can send a payment" \
  --description "..." \
  --priority High \
  --labels payments,p2p
```

### Issue Types
- `Epic` — large feature group
- `Story` — user-facing feature
- `Bug` — defect report
- `Task` — technical or non-user-facing work
