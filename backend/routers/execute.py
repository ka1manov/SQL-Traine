import logging
from fastapi import APIRouter, Request
from models.schemas import ExecuteRequest, ExecuteResponse
from services.sandbox import create_sandbox, execute_in_sandbox
from services.dependencies import get_user_id
from db.connection import get_pool

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["execute"])


@router.post("/execute", response_model=ExecuteResponse)
async def execute_sql(req: ExecuteRequest, request: Request):
    session_id = await create_sandbox(req.session_id)
    result = await execute_in_sandbox(session_id, req.sql)

    # Save to history
    user_id = await get_user_id(request)
    if user_id:
        try:
            pool = await get_pool()
            async with pool.acquire() as conn:
                await conn.execute(
                    """INSERT INTO query_history (user_id, sql_text, execution_time_ms, row_count, had_error)
                       VALUES ($1, $2, $3, $4, $5)""",
                    user_id, req.sql, result.get("execution_time_ms", 0),
                    result.get("row_count", 0), result.get("error") is not None,
                )
        except Exception as e:
            logger.warning("Failed to save query history: %s", e)

    return ExecuteResponse(**result)
