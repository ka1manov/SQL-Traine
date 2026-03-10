from fastapi import APIRouter, Request, HTTPException
from models.schemas import ProgressEntry
from services.dependencies import get_user_id, require_user_id
from db.connection import get_pool

router = APIRouter(prefix="/api", tags=["progress"])


@router.get("/progress")
async def get_progress(request: Request):
    user_id = await get_user_id(request)
    if not user_id:
        return []
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT task_id, solved, best_match_pct, attempts FROM user_progress WHERE user_id = $1",
            user_id,
        )
        return [dict(r) for r in rows]


@router.post("/progress")
async def update_progress(entry: ProgressEntry, request: Request):
    user_id = await require_user_id(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        existing = await conn.fetchrow(
            "SELECT * FROM user_progress WHERE user_id = $1 AND task_id = $2",
            user_id, entry.task_id,
        )
        if existing:
            await conn.execute("""
                UPDATE user_progress
                SET attempts = attempts + 1,
                    best_match_pct = GREATEST(best_match_pct, $3),
                    solved = solved OR $4,
                    last_attempt_at = NOW()
                WHERE user_id = $1 AND task_id = $2
            """, user_id, entry.task_id, entry.best_match_pct, entry.solved)
        else:
            await conn.execute("""
                INSERT INTO user_progress (user_id, task_id, solved, best_match_pct, attempts)
                VALUES ($1, $2, $3, $4, $5)
            """, user_id, entry.task_id, entry.solved, entry.best_match_pct, entry.attempts)

        row = await conn.fetchrow(
            "SELECT task_id, solved, best_match_pct, attempts FROM user_progress WHERE user_id = $1 AND task_id = $2",
            user_id, entry.task_id,
        )
        return dict(row)
