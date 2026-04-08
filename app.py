"""
FastAPI application exposing the EmailTriageEnv as an OpenEnv-compliant HTTP API.
Designed for deployment on Hugging Face Spaces (port 7860).
"""

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from env import EmailTriageEnv, EmailAction

app = FastAPI(
    title="Email Triage OpenEnv",
    description=(
        "An OpenEnv-compliant environment where an AI agent triages emails "
        "across three tasks of increasing difficulty."
    ),
    version="1.0.0",
)

# One shared environment instance (stateful per session)
env = EmailTriageEnv()


@app.get("/")
def health():
    return {"status": "ok", "env": "email-triage-env", "version": "1.0.0"}


@app.post("/reset")
def reset(task_id: str = Query("task_easy", enum=["task_easy", "task_medium", "task_hard"])):
    """Reset the environment and return the first observation."""
    obs = env.reset(task_id=task_id)
    return obs.model_dump()


@app.post("/step")
def step(action: EmailAction):
    """Take one step in the environment."""
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.model_dump(),
        "reward": reward.model_dump(),
        "done": done,
        "info": info,
    }


@app.get("/state")
def state():
    """Return the current internal state of the environment."""
    return env.state()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
