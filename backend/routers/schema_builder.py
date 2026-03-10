import uuid
import asyncio
import logging
from fastapi import APIRouter
from models.schemas import ValidateDDLRequest, ValidateDDLResponse
from db.connection import get_pool

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["schema-builder"])

DANGEROUS_KEYWORDS = {
    "DROP DATABASE", "GRANT ", "REVOKE ", "SET ROLE",
    "SET SESSION AUTHORIZATION", "ALTER SYSTEM", "COPY ",
    "pg_read", "pg_write", "lo_import", "lo_export",
}


@router.post("/schema-builder/validate", response_model=ValidateDDLResponse)
async def validate_ddl(req: ValidateDDLRequest):
    ddl = req.ddl.strip()
    if not ddl:
        return ValidateDDLResponse(valid=False, error="Empty DDL", details=None)

    upper = ddl.upper()
    for kw in DANGEROUS_KEYWORDS:
        if kw.upper() in upper:
            return ValidateDDLResponse(valid=False, error=f"Blocked keyword: {kw.strip()}", details=None)

    schema_name = f"ddl_validate_{uuid.uuid4().hex[:12]}"
    pool = await get_pool()
    try:
        async with pool.acquire() as conn:
            await conn.execute(f'CREATE SCHEMA "{schema_name}"')
            try:
                await conn.execute(f'SET search_path TO "{schema_name}"')
                await asyncio.wait_for(conn.execute(ddl), timeout=5.0)
                tables = await conn.fetch(
                    "SELECT table_name FROM information_schema.tables WHERE table_schema = $1",
                    schema_name,
                )
                count = len(tables)
                table_names = ", ".join(r["table_name"] for r in tables)
                return ValidateDDLResponse(
                    valid=True,
                    error=None,
                    details=f"Created {count} table(s): {table_names}" if count > 0 else "DDL executed successfully",
                )
            except asyncio.TimeoutError:
                return ValidateDDLResponse(valid=False, error="DDL execution timed out (5s limit)", details=None)
            except Exception as e:
                return ValidateDDLResponse(valid=False, error=str(e), details=None)
            finally:
                await conn.execute('SET search_path TO public')
                await conn.execute(f'DROP SCHEMA IF EXISTS "{schema_name}" CASCADE')
    except Exception as e:
        logger.error("Schema validation failed: %s", e)
        return ValidateDDLResponse(valid=False, error=str(e), details=None)
