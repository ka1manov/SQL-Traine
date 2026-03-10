from fastapi import APIRouter, Request, HTTPException
from models.schemas import BookmarkRequest
from services.dependencies import get_user_id, require_user_id
from db.connection import get_pool

router = APIRouter(prefix="/api", tags=["streaks"])


@router.get("/streaks")
async def get_streaks(request: Request):
    user_id = await get_user_id(request)
    if not user_id:
        return {"current_streak": 0, "best_streak": 0, "days": []}
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT completed_date::text AS date, task_id FROM daily_streaks WHERE user_id = $1 ORDER BY completed_date DESC",
            user_id,
        )
        days = [dict(r) for r in rows]

        # Calculate streaks
        if not days:
            return {"current_streak": 0, "best_streak": 0, "days": days}

        from datetime import date, timedelta
        dates = sorted(set(d["date"] for d in days))
        date_objs = [date.fromisoformat(d) for d in dates]

        current = 1
        best = 1
        today = date.today()

        # Current streak (must include today or yesterday)
        if date_objs and (today - date_objs[-1]).days > 1:
            current = 0
        else:
            for i in range(len(date_objs) - 1, 0, -1):
                if (date_objs[i] - date_objs[i - 1]).days == 1:
                    current += 1
                else:
                    break

        # Best streak
        streak = 1
        for i in range(1, len(date_objs)):
            if (date_objs[i] - date_objs[i - 1]).days == 1:
                streak += 1
                best = max(best, streak)
            else:
                streak = 1

        return {"current_streak": current, "best_streak": best, "days": days}


@router.post("/streaks")
async def record_streak(req: BookmarkRequest, request: Request):
    user_id = await require_user_id(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO daily_streaks (user_id, completed_date, task_id) VALUES ($1, CURRENT_DATE, $2) ON CONFLICT DO NOTHING",
            user_id, req.task_id,
        )
    return {"ok": True}
