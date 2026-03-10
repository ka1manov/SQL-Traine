from fastapi import APIRouter, Request
from models.schemas import AssignmentStepProgress
from services.dependencies import get_user_id, require_user_id
from db.connection import get_pool

router = APIRouter(prefix="/api", tags=["assignment-progress"])


@router.get("/assignments/progress")
async def get_assignment_progress(request: Request):
    user_id = await get_user_id(request)
    if not user_id:
        return []
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT assignment_id, step, completed FROM assignment_progress WHERE user_id = $1",
            user_id,
        )
        return [dict(r) for r in rows]


@router.post("/assignments/progress")
async def update_assignment_progress(entry: AssignmentStepProgress, request: Request):
    user_id = await require_user_id(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO assignment_progress (user_id, assignment_id, step, completed, completed_at)
            VALUES ($1, $2, $3, $4, CASE WHEN $4 THEN NOW() ELSE NULL END)
            ON CONFLICT (user_id, assignment_id, step)
            DO UPDATE SET completed = EXCLUDED.completed,
                completed_at = CASE WHEN EXCLUDED.completed THEN NOW() ELSE assignment_progress.completed_at END
        """, user_id, entry.assignment_id, entry.step, entry.completed)
        row = await conn.fetchrow(
            "SELECT assignment_id, step, completed FROM assignment_progress WHERE user_id = $1 AND assignment_id = $2 AND step = $3",
            user_id, entry.assignment_id, entry.step,
        )
        return dict(row)
