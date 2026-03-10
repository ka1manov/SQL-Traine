from datetime import date
from fastapi import APIRouter
from data.tasks import TASKS
from models.schemas import TaskOut

router = APIRouter(prefix="/api", tags=["daily"])


@router.get("/daily", response_model=TaskOut)
async def daily_challenge():
    today = date.today()
    idx = today.toordinal() % len(TASKS)
    task = TASKS[idx]
    return TaskOut(**{k: v for k, v in task.__dict__.items() if k != 'solution_sql'})
