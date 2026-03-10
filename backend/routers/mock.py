import uuid
import random
from datetime import datetime
from fastapi import APIRouter, HTTPException
from models.schemas import MockStartRequest, MockSession, MockEndRequest, MockResult
from data.tasks import TASKS

router = APIRouter(prefix="/api/mock", tags=["mock"])

_sessions: dict[str, dict] = {}


@router.post("/start", response_model=MockSession)
async def start_mock(req: MockStartRequest):
    candidates = TASKS
    if req.difficulty:
        candidates = [t for t in candidates if t.difficulty == req.difficulty]
    if not candidates:
        raise HTTPException(status_code=400, detail="No tasks match the selected difficulty")

    selected = random.sample(candidates, min(5, len(candidates)))
    session_id = uuid.uuid4().hex[:12]
    started_at = datetime.utcnow().isoformat()

    session = MockSession(
        session_id=session_id,
        task_ids=[t.id for t in selected],
        time_limit=1800,
        started_at=started_at,
    )
    _sessions[session_id] = {"session": session, "started_at": started_at}
    return session


@router.post("/end", response_model=MockResult)
async def end_mock(req: MockEndRequest):
    session_data = _sessions.pop(req.session_id, None)
    if session_data:
        total_tasks = len(session_data["session"].task_ids)
    else:
        total_tasks = max(len(req.results), 1)

    tasks_solved = sum(1 for r in req.results if r.get("correct"))
    total_score = round(
        sum(r.get("match_pct", 0) for r in req.results) / max(total_tasks, 1), 1
    )

    time_used = None
    if req.results:
        time_used = req.results[0].get("time_used")

    return MockResult(
        total_score=total_score,
        tasks_solved=tasks_solved,
        total_tasks=total_tasks,
        time_used=time_used,
        details=req.results,
    )
