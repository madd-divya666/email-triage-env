from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, Any


class EmailObservation(BaseModel):
    email_id: str
    subject: str
    body: str
    sender: str
    task_id: str
    step_number: int
    total_steps: int


class EmailAction(BaseModel):
    # Task 1 (easy)
    urgency: Optional[Literal["urgent", "not_urgent"]] = None
    # Task 2 (medium)
    category: Optional[Literal[
        "billing", "technical_support", "complaint", "general_inquiry", "spam"
    ]] = None
    # Task 3 (hard) — also uses category above
    priority: Optional[int] = Field(None, ge=1, le=5, description="1=critical, 5=low")
    routing_department: Optional[Literal[
        "finance", "tech_team", "customer_relations", "general_support", "spam_filter"
    ]] = None


class EmailReward(BaseModel):
    value: float = Field(..., gt=0.0, lt=1.0)
    breakdown: Dict[str, float] = {}
    feedback: str = ""
