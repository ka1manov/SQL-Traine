from fastapi import APIRouter, Request, HTTPException
from models.schemas import FlashcardReview, FlashcardState
from services.dependencies import get_user_id, require_user_id
from db.connection import get_pool

router = APIRouter(prefix="/api", tags=["flashcards"])


@router.get("/flashcards/progress")
async def get_flashcard_progress(request: Request):
    user_id = await get_user_id(request)
    if not user_id:
        return []
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """SELECT card_id, ease_factor, interval_days, repetitions, next_review::text
               FROM flashcard_progress WHERE user_id = $1""",
            user_id,
        )
        return [dict(r) for r in rows]


@router.post("/flashcards/review")
async def review_flashcard(review: FlashcardReview, request: Request):
    """SM-2 spaced repetition algorithm."""
    user_id = await require_user_id(request)

    pool = await get_pool()
    async with pool.acquire() as conn:
        existing = await conn.fetchrow(
            "SELECT * FROM flashcard_progress WHERE user_id = $1 AND card_id = $2",
            user_id, review.card_id,
        )

        if existing:
            ef = existing["ease_factor"]
            interval = existing["interval_days"]
            reps = existing["repetitions"]
        else:
            ef = 2.5
            interval = 1
            reps = 0

        q = max(0, min(5, review.quality))

        if q >= 3:  # Correct
            if reps == 0:
                interval = 1
            elif reps == 1:
                interval = 6
            else:
                interval = round(interval * ef)
            reps += 1
        else:  # Incorrect
            reps = 0
            interval = 1

        ef = max(1.3, ef + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)))

        await conn.execute("""
            INSERT INTO flashcard_progress (user_id, card_id, ease_factor, interval_days, repetitions, next_review)
            VALUES ($1, $2, $3, $4, $5, NOW() + make_interval(days => $4::int))
            ON CONFLICT (user_id, card_id) DO UPDATE SET
                ease_factor = $3, interval_days = $4, repetitions = $5,
                next_review = NOW() + make_interval(days => $4::int)
        """, user_id, review.card_id, ef, interval, reps)

    return {"ease_factor": ef, "interval_days": interval, "repetitions": reps}
