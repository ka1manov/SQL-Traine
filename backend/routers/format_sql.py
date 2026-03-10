from fastapi import APIRouter
from models.schemas import FormatRequest, FormatResponse
import sqlparse

router = APIRouter(prefix="/api", tags=["format"])


@router.post("/format", response_model=FormatResponse)
async def format_sql(req: FormatRequest):
    formatted = sqlparse.format(
        req.sql,
        reindent=True,
        keyword_case="upper",
        indent_width=2,
        strip_comments=False,
    )
    return FormatResponse(formatted=formatted)
