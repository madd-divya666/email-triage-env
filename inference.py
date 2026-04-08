"""
Baseline inference script for Email Triage OpenEnv.

Uses the OpenAI client to run an LLM agent against all three tasks
and emits structured [START] / [STEP] / [END] logs to stdout.

Required environment variables:
  API_BASE_URL  — LLM endpoint base URL
  MODEL_NAME    — model identifier
  HF_TOKEN      — Hugging Face / API key

Usage:
  python inference.py
"""

import os
import json
import requests
import httpx
from openai import OpenAI

# ------------------------------------------------------------------
# Config from environment
# ------------------------------------------------------------------
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.environ.get("HF_TOKEN", "")
ENV_BASE_URL = os.environ.get("ENV_BASE_URL", "http://localhost:7860")

client = None


def get_client():
    global client
    if client is None:
        client = OpenAI(
            api_key=HF_TOKEN,
            base_url=API_BASE_URL,
            http_client=httpx.Client(),
        )
    return client

TASKS = ["task_easy", "task_medium", "task_hard"]

SYSTEM_PROMPTS = {
    "task_easy": (
        "You are an email triage assistant. For each email, decide if it is 'urgent' or 'not_urgent'. "
        "Respond ONLY with a JSON object: {\"urgency\": \"urgent\"} or {\"urgency\": \"not_urgent\"}."
    ),
    "task_medium": (
        "You are an email triage assistant. Classify each email into exactly one category: "
        "billing, technical_support, complaint, general_inquiry, or spam. "
        "Respond ONLY with a JSON object: {\"category\": \"<category>\"}."
    ),
    "task_hard": (
        "You are an email triage assistant. For each email provide:\n"
        "- category: billing | technical_support | complaint | general_inquiry | spam\n"
        "- priority: integer 1 (critical) to 5 (low)\n"
        "- routing_department: finance | tech_team | customer_relations | general_support | spam_filter\n"
        "Respond ONLY with a JSON object with keys: category, priority, routing_department."
    ),
}


def call_env(method: str, path: str, payload: dict = None):
    url = f"{ENV_BASE_URL}{path}"
    if method == "GET":
        r = requests.get(url, params=payload or {}, timeout=30)
    else:
        r = requests.post(url, json=payload or {}, params=payload if method == "POST_QUERY" else None, timeout=30)
    r.raise_for_status()
    return r.json()


def reset_env(task_id: str):
    r = requests.post(f"{ENV_BASE_URL}/reset", params={"task_id": task_id}, timeout=30)
    r.raise_for_status()
    return r.json()


def step_env(action: dict):
    r = requests.post(f"{ENV_BASE_URL}/step", json=action, timeout=30)
    r.raise_for_status()
    return r.json()


def llm_action(task_id: str, obs: dict) -> dict:
    """Ask the LLM to produce an action for the current observation."""
    user_msg = (
        f"From: {obs['sender']}\n"
        f"Subject: {obs['subject']}\n\n"
        f"{obs['body']}"
    )
    response = get_client().chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPTS[task_id]},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.0,
        max_tokens=100,
    )
    raw = response.choices[0].message.content.strip()
    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw)


def run_task(task_id: str):
    obs = reset_env(task_id)
    total_steps = obs["total_steps"]

    log_start = {"type": "START", "task_id": task_id, "total_steps": total_steps}
    print(f"[START] {json.dumps(log_start)}", flush=True)

    step_num = 0
    total_reward = 0.0

    while True:
        if obs.get("email_id") == "DONE":
            break

        action = llm_action(task_id, obs)
        result = step_env(action)

        reward_val = result["reward"]["value"]
        total_reward += reward_val
        step_num += 1

        log_step = {
            "type": "STEP",
            "task_id": task_id,
            "step": step_num,
            "email_id": obs["email_id"],
            "action": action,
            "reward": reward_val,
            "feedback": result["reward"]["feedback"],
            "done": result["done"],
        }
        print(f"[STEP] {json.dumps(log_step)}", flush=True)

        if result["done"]:
            break
        obs = result["observation"]

    mean_score = round(total_reward / step_num, 4) if step_num > 0 else 0.0
    log_end = {
        "type": "END",
        "task_id": task_id,
        "steps_completed": step_num,
        "total_reward": round(total_reward, 4),
        "mean_score": mean_score,
    }
    print(f"[END] {json.dumps(log_end)}", flush=True)
    return mean_score


def main():
    all_scores = {}
    for task_id in TASKS:
        score = run_task(task_id)
        all_scores[task_id] = score

    summary = {
        "type": "SUMMARY",
        "scores": all_scores,
        "overall_mean": round(sum(all_scores.values()) / len(all_scores), 4),
    }
    print(f"[SUMMARY] {json.dumps(summary)}", flush=True)


if __name__ == "__main__":
    main()
