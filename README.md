---
title: Email Triage Env
emoji: ⚡
colorFrom: red
colorTo: gray
sdk: docker
pinned: false
license: mit
short_description: Email triage environment for OpenEnv hackathon
---

# Email Triage OpenEnv

An **OpenEnv-compliant** environment where an AI agent triages a realistic inbox of emails.
Built for the [OpenEnv × Scaler × Meta PyTorch Hackathon](https://scaler.com).

---

## Tasks

| Task ID | Difficulty | Description | Reward |
|---|---|---|---|
| `task_easy` | Easy | Classify each email as `urgent` or `not_urgent` | 1.0 = correct, 0.0 = wrong |
| `task_medium` | Medium | Classify into one of 5 categories | 1.0 = correct, 0.0 = wrong |
| `task_hard` | Hard | Category + priority (1–5) + routing department | Weighted: 40% category, 30% priority, 30% routing |

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/reset?task_id=task_easy` | Start a new episode |
| POST | `/step` | Submit an action, get next observation + reward |
| GET | `/state` | Current environment state |
