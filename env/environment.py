from typing import Tuple, Dict, Any
from .models import EmailObservation, EmailAction, EmailReward
from .data import EMAILS


VALID_TASK_IDS = {"task_easy", "task_medium", "task_hard"}

DEPT_FOR_CATEGORY = {
    "billing": "finance",
    "technical_support": "tech_team",
    "complaint": "customer_relations",
    "general_inquiry": "general_support",
    "spam": "spam_filter",
}


class EmailTriageEnv:
    """
    OpenEnv-compliant Email Triage environment.

    Three tasks of increasing difficulty:
      task_easy   — binary urgency classification
      task_medium — 5-class category classification
      task_hard   — category + priority + routing department
    """

    def __init__(self):
        self._task_id: str = "task_easy"
        self._emails = EMAILS
        self._step_idx: int = 0
        self._done: bool = False
        self._episode_rewards: list[float] = []

    # ------------------------------------------------------------------
    # OpenEnv interface
    # ------------------------------------------------------------------

    def reset(self, task_id: str = "task_easy") -> EmailObservation:
        if task_id not in VALID_TASK_IDS:
            raise ValueError(f"task_id must be one of {VALID_TASK_IDS}")
        self._task_id = task_id
        self._step_idx = 0
        self._done = False
        self._episode_rewards = []
        return self._make_observation()

    def step(self, action: EmailAction) -> Tuple[EmailObservation, EmailReward, bool, Dict[str, Any]]:
        if self._done:
            raise RuntimeError("Episode is done. Call reset() to start a new episode.")

        email = self._emails[self._step_idx]
        reward = self._grade(action, email)
        self._episode_rewards.append(reward.value)
        self._step_idx += 1

        done = self._step_idx >= len(self._emails)
        self._done = done

        if done:
            obs = EmailObservation(
                email_id="DONE",
                subject="",
                body="",
                sender="",
                task_id=self._task_id,
                step_number=self._step_idx,
                total_steps=len(self._emails),
            )
        else:
            obs = self._make_observation()

        info = {
            "email_id": email["email_id"],
            "episode_mean_reward": sum(self._episode_rewards) / len(self._episode_rewards),
        }
        return obs, reward, done, info

    def state(self) -> Dict[str, Any]:
        return {
            "task_id": self._task_id,
            "step_index": self._step_idx,
            "total_steps": len(self._emails),
            "done": self._done,
            "episode_rewards": list(self._episode_rewards),
            "episode_mean_reward": (
                sum(self._episode_rewards) / len(self._episode_rewards)
                if self._episode_rewards else 0.0
            ),
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _make_observation(self) -> EmailObservation:
        email = self._emails[self._step_idx]
        return EmailObservation(
            email_id=email["email_id"],
            subject=email["subject"],
            body=email["body"],
            sender=email["sender"],
            task_id=self._task_id,
            step_number=self._step_idx + 1,
            total_steps=len(self._emails),
        )

    def _grade(self, action: EmailAction, email: dict) -> EmailReward:
        if self._task_id == "task_easy":
            return self._grade_easy(action, email)
        elif self._task_id == "task_medium":
            return self._grade_medium(action, email)
        else:
            return self._grade_hard(action, email)

    def _grade_easy(self, action: EmailAction, email: dict) -> EmailReward:
        gt = email["easy_label"]
        pred = action.urgency
        if pred is None:
            return EmailReward(value=0.01, breakdown={"urgency": 0.01}, feedback="No urgency provided.")
        correct = 0.99 if pred == gt else 0.01
        feedback = "Correct!" if pred == gt else f"Wrong. Expected '{gt}', got '{pred}'."
        return EmailReward(value=correct, breakdown={"urgency": correct}, feedback=feedback)

    def _grade_medium(self, action: EmailAction, email: dict) -> EmailReward:
        gt = email["medium_label"]
        pred = action.category
        if pred is None:
            return EmailReward(value=0.01, breakdown={"category": 0.01}, feedback="No category provided.")
        correct = 0.99 if pred == gt else 0.01
        feedback = "Correct!" if pred == gt else f"Wrong. Expected '{gt}', got '{pred}'."
        return EmailReward(value=correct, breakdown={"category": correct}, feedback=feedback)

    def _grade_hard(self, action: EmailAction, email: dict) -> EmailReward:
        gt = email["hard_label"]
        breakdown: Dict[str, float] = {}
        feedback_parts = []

        # Category (weight 0.40)
        cat_score = 0.0
        if action.category is not None:
            cat_score = 1.0 if action.category == gt["category"] else 0.0
            cat_fb = "correct" if cat_score else f"wrong (expected {gt['category']})"
            feedback_parts.append(f"Category: {cat_fb}")
        else:
            feedback_parts.append("Category: missing")
        breakdown["category"] = cat_score

        # Priority (weight 0.30) — partial credit for close answers
        pri_score = 0.0
        if action.priority is not None:
            diff = abs(action.priority - gt["priority"])
            pri_score = max(0.0, 1.0 - diff * 0.25)
            pri_fb = "correct" if diff == 0 else f"off by {diff} (expected {gt['priority']})"
            feedback_parts.append(f"Priority: {pri_fb}")
        else:
            feedback_parts.append("Priority: missing")
        breakdown["priority"] = pri_score

        # Routing (weight 0.30)
        route_score = 0.0
        if action.routing_department is not None:
            route_score = 1.0 if action.routing_department == gt["routing_department"] else 0.0
            route_fb = "correct" if route_score else f"wrong (expected {gt['routing_department']})"
            feedback_parts.append(f"Routing: {route_fb}")
        else:
            feedback_parts.append("Routing: missing")
        breakdown["routing"] = route_score

        total = round(0.40 * cat_score + 0.30 * pri_score + 0.30 * route_score, 4)
        total = max(0.01, min(0.99, total))
        return EmailReward(
            value=total,
            breakdown=breakdown,
            feedback=" | ".join(feedback_parts),
        )
