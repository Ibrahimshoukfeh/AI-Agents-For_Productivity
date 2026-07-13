from pydantic import BaseModel


class CommuteSummary(BaseModel):
    start: str
    destination: str
    total_duration_minutes: int


class CommuteTimes(BaseModel):
    departing_at: str
    arriving_at: str


class QuickCommuteResponse(BaseModel):
    summary: CommuteSummary
    times: CommuteTimes
    instructions: list[str]
