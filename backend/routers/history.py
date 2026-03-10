from fastapi import APIRouter, Request
from services.auth import get_user_id_from_token
from db.connection import get_pool

router = APIRouter(prefix="/api", tags=["history"])


async def _get_user_id(request: Request) -> int | None:
    auth = request.headers.get("authorization", "")
    if auth.startswith("Bearer "):
        return await get_user_id_from_token(auth[7:])
    return None


@router.get("/history")
async def get_history(request: Request, limit: int = 50):
    user_id = await _get_user_id(request)
    if not user_id:
        return []
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """SELECT id, sql_text, execution_time_ms, row_count, had_error, created_at::text
               FROM query_history WHERE user_id = $1
               ORDER BY created_at DESC LIMIT $2""",
            user_id, min(limit, 200),
        )
        return [dict(r) for r in rows]


@router.delete("/history")
async def clear_history(request: Request):
    user_id = await _get_user_id(request)
    if not user_id:
        return {"cleared": 0}
    pool = await get_pool()
    async with pool.acquire() as conn:
        result = await conn.execute("DELETE FROM query_history WHERE user_id = $1", user_id)
        count = int(result.split()[-1]) if result else 0
        return {"cleared": count}
