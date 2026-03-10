from fastapi import APIRouter
from db.connection import get_pool

router = APIRouter(prefix="/api", tags=["leaderboard"])


@router.get("/leaderboard")
async def get_leaderboard(limit: int = 20):
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT u.username,
                   COUNT(CASE WHEN p.solved THEN 1 END) AS tasks_solved,
                   SUM(p.attempts) AS total_attempts,
                   ROUND(AVG(p.best_match_pct)::numeric, 1) AS avg_match_pct
            FROM app_users u
            JOIN user_progress p ON u.id = p.user_id
            GROUP BY u.id, u.username
            ORDER BY tasks_solved DESC, avg_match_pct DESC
            LIMIT $1
        """, min(limit, 100))
        return [dict(r) for r in rows]
