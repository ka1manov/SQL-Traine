from fastapi import APIRouter, Request
from models.schemas import InterviewProgressEntry
from services.dependencies import get_user_id, require_user_id
from db.connection import get_pool

router = APIRouter(prefix="/api", tags=["interview-progress"])


@router.get("/interview-questions/progress")
async def get_interview_progress(request: Request):
    user_id = await get_user_id(request)
    if not user_id:
        return []
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT question_id, solved, best_match_pct, attempts FROM interview_progress WHERE user_id = $1",
            user_id,
        )
        return [dict(r) for r in rows]


@router.post("/interview-questions/progress")
async def update_interview_progress(entry: InterviewProgressEntry, request: Request):
    user_id = await require_user_id(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        existing = await conn.fetchrow(
            "SELECT * FROM interview_progress WHERE user_id = $1 AND question_id = $2",
            user_id, entry.question_id,
        )
        if existing:
            await conn.execute("""
                UPDATE interview_progress
                SET attempts = attempts + 1,
                    best_match_pct = GREATEST(best_match_pct, $3),
                    solved = solved OR $4,
                    last_attempt_at = NOW()
                WHERE user_id = $1 AND question_id = $2
            """, user_id, entry.question_id, entry.best_match_pct, entry.solved)
        else:
            await conn.execute("""
                INSERT INTO interview_progress (user_id, question_id, solved, best_match_pct, attempts)
                VALUES ($1, $2, $3, $4, $5)
            """, user_id, entry.question_id, entry.solved, entry.best_match_pct, entry.attempts)

        row = await conn.fetchrow(
            "SELECT question_id, solved, best_match_pct, attempts FROM interview_progress WHERE user_id = $1 AND question_id = $2",
            user_id, entry.question_id,
        )
        return dict(row)
