import uuid
import random
import time
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from models.schemas import MockStartRequest, MockSession, MockEndRequest, MockResult
from data.tasks import TASKS

router = APIRouter(prefix="/api/mock", tags=["mock"])

_sessions: dict[str, dict] = {}

# Clean up sessions older than 2 hours
_SESSION_MAX_AGE = 7200


def _cleanup_stale_sessions():
    now = time.monotonic()
    stale = [k for k, v in _sessions.items() if now - v.get("created_mono", 0) > _SESSION_MAX_AGE]
    for k in stale:
        _sessions.pop(k, None)


@router.post("/start", response_model=MockSession)
async def start_mock(req: MockStartRequest):
    _cleanup_stale_sessions()

    candidates = TASKS
    if req.difficulty:
        candidates = [t for t in candidates if t.difficulty == req.difficulty]
    if not candidates:
        raise HTTPException(status_code=400, detail="No tasks match the selected difficulty")

    selected = random.sample(candidates, min(5, len(candidates)))
    session_id = uuid.uuid4().hex[:12]
    started_at = datetime.now(timezone.utc).isoformat()

    session = MockSession(
        session_id=session_id,
        task_ids=[t.id for t in selected],
        time_limit=1800,
        started_at=started_at,
    )
    _sessions[session_id] = {"session": session, "started_at": started_at, "created_mono": time.monotonic()}
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
