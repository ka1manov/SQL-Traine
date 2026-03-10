import hashlib
from datetime import date
from fastapi import APIRouter
from data.tasks import TASKS, TASKS_BY_ID
from models.schemas import TaskOut

router = APIRouter(prefix="/api", tags=["daily"])


@router.get("/daily", response_model=TaskOut)
async def daily_challenge():
    today = date.today().isoformat()
    h = int(hashlib.md5(today.encode()).hexdigest(), 16)
    task = TASKS[h % len(TASKS)]
    return TaskOut(**task.__dict__)
