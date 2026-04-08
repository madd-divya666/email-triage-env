# Email Triage OpenEnv

An **OpenEnv-compliant** environment where an AI agent triages a realistic inbox of emails.
Built for the [OpenEnv × Scaler × Meta PyTorch Hackathon](https://scaler.com).

---

## Environment Description

The agent receives one email at a time and must triage it. The environment contains **10 real-world style emails** spanning system alerts, billing disputes, support requests, complaints, and spam.

---

## Tasks

| Task ID | Difficulty | Description | Reward |
|---|---|---|---|
| `task_easy` | Easy | Classify each email as `urgent` or `not_urgent` | 1.0 = correct, 0.0 = wrong |
| `task_medium` | Medium | Classify into one of 5 categories | 1.0 = correct, 0.0 = wrong |
| `task_hard` | Hard | Category + priority (1–5) + routing department | Weighted: 40% category, 30% priority, 30% routing |

---

## Observation Space

```json
{
  "email_id":    "string  — unique identifier",
  "subject":     "string  — email subject line",
  "body":        "string  — email body text",
  "sender":      "string  — sender email address",
  "task_id":     "string  — current task",
  "step_number": "int     — current step (1-indexed)",
  "total_steps": "int     — total emails in episode (10)"
}
```

## Action Space

```json
{
  "urgency":            "urgent | not_urgent              (task_easy)",
  "category":           "billing | technical_support | complaint | general_inquiry | spam  (task_medium/hard)",
  "priority":           "1 (critical) to 5 (low)          (task_hard)",
  "routing_department": "finance | tech_team | customer_relations | general_support | spam_filter  (task_hard)"
}
```

## Reward

- Range: **0.0 – 1.0** per step
- Partial credit on `task_hard` (priority score is graded by proximity)
- Episode score = mean reward across all 10 steps

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/reset?task_id=task_easy` | Start a new episode |
| POST | `/step` | Submit an action, get next observation + reward |
| GET | `/state` | Current environment state |

---

## Setup & Usage

### Local

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 7860
```

### Docker

```bash
docker build -t email-triage-env .
docker run -p 7860:7860 email-triage-env
```

### Run Baseline Inference

```bash
export API_BASE_URL="https://api.openai.com/v1"
export MODEL_NAME="gpt-4o-mini"
export HF_TOKEN="your-api-key"
export ENV_BASE_URL="http://localhost:7860"

python inference.py
```

---

## Baseline Scores

Measured with `gpt-4o-mini` (temperature=0):

| Task | Score |
|---|---|
| task_easy | ~0.90 |
| task_medium | ~0.80 |
| task_hard | ~0.72 |

---

## Pre-submission Checklist

- [x] HF Space deploys and returns 200 on `/`
- [x] `/reset` responds with valid observation
- [x] OpenEnv spec: typed Pydantic models, step/reset/state endpoints
- [x] `openenv.yaml` present
- [x] Dockerfile builds and runs cleanly
- [x] 3 tasks with graders (easy → medium → hard), scores in 0.0–1.0
- [x] Meaningful reward with partial progress (task_hard)
- [x] `inference.py` in root, uses OpenAI client, emits [START]/[STEP]/[END] logs
- [x] README with environment description, spaces, setup, baseline scores
