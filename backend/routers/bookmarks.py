from fastapi import APIRouter, Request, HTTPException
from models.schemas import BookmarkRequest
from services.auth import get_user_id_from_token
from db.connection import get_pool

router = APIRouter(prefix="/api", tags=["bookmarks"])


async def _get_user_id(request: Request) -> int | None:
    auth = request.headers.get("authorization", "")
    if auth.startswith("Bearer "):
        return await get_user_id_from_token(auth[7:])
    return None


@router.get("/bookmarks")
async def get_bookmarks(request: Request):
    user_id = await _get_user_id(request)
    if not user_id:
        return []
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT task_id, created_at::text FROM user_bookmarks WHERE user_id = $1 ORDER BY created_at DESC",
            user_id,
        )
        return [dict(r) for r in rows]


@router.post("/bookmarks")
async def add_bookmark(req: BookmarkRequest, request: Request):
    user_id = await _get_user_id(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="Login required")
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO user_bookmarks (user_id, task_id) VALUES ($1, $2) ON CONFLICT DO NOTHING",
            user_id, req.task_id,
        )
    return {"ok": True}


@router.delete("/bookmarks/{task_id}")
async def remove_bookmark(task_id: int, request: Request):
    user_id = await _get_user_id(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="Login required")
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "DELETE FROM user_bookmarks WHERE user_id = $1 AND task_id = $2",
            user_id, task_id,
        )
    return {"ok": True}
