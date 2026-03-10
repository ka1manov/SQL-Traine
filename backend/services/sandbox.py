import uuid
import asyncio
import time
import asyncpg
from db.connection import get_pool

BLOCKED_KEYWORDS = {
    "DROP DATABASE", "DROP SCHEMA", "CREATE DATABASE", "TRUNCATE",
    "ALTER SYSTEM", "COPY ", "pg_read", "pg_write", "lo_import", "lo_export",
    "pg_catalog", "information_schema",
}

PUBLIC_TABLES = [
    "departments", "employees", "customers", "products", "orders",
    "invoices", "salaries_log", "subscriptions", "streams", "bookings",
    "ab_tests", "clickstream",
]


def validate_sql(sql: str) -> str | None:
    upper = sql.upper().strip()
    for kw in BLOCKED_KEYWORDS:
        if kw.upper() in upper:
            return f"Blocked keyword: {kw}"
    if "PUBLIC." in upper:
        return "Direct access to public schema is not allowed in sandbox"
    return None


async def create_sandbox(session_id: str | None = None) -> str:
    if not session_id:
        session_id = uuid.uuid4().hex[:12]
    schema = f"sandbox_{session_id}"
    pool = await get_pool()
    async with pool.acquire() as conn:
        exists = await conn.fetchval(
            "SELECT 1 FROM information_schema.schemata WHERE schema_name = $1", schema
        )
        if exists:
            return session_id
        await conn.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema}"')
        for table in PUBLIC_TABLES:
            await conn.execute(
                f'CREATE TABLE IF NOT EXISTS "{schema}"."{table}" (LIKE public."{table}" INCLUDING ALL)'
            )
            await conn.execute(
                f'INSERT INTO "{schema}"."{table}" SELECT * FROM public."{table}"'
            )
    return session_id


async def execute_in_sandbox(session_id: str, sql: str) -> dict:
    error = validate_sql(sql)
    if error:
        return {"columns": [], "rows": [], "row_count": 0, "error": error, "execution_time_ms": 0}

    schema = f"sandbox_{session_id}"
    pool = await get_pool()
    start = time.monotonic()
    try:
        async with pool.acquire() as conn:
            await conn.execute(f'SET search_path TO "{schema}"')
            stmt = sql.strip().rstrip(";").strip()
            upper = stmt.upper()
            if upper.startswith(("INSERT", "UPDATE", "DELETE", "CREATE", "ALTER")):
                status = await asyncio.wait_for(conn.execute(sql), timeout=5.0)
                elapsed = int((time.monotonic() - start) * 1000)
                return {"columns": ["status"], "rows": [[status]], "row_count": 1, "error": None, "execution_time_ms": elapsed}
            result = await asyncio.wait_for(conn.fetch(sql), timeout=5.0)
            elapsed = int((time.monotonic() - start) * 1000)
            if result:
                columns = list(result[0].keys())
                rows = [list(r.values()) for r in result]
            else:
                columns = []
                rows = []
            return {"columns": columns, "rows": rows, "row_count": len(rows), "error": None, "execution_time_ms": elapsed}
    except asyncio.TimeoutError:
        elapsed = int((time.monotonic() - start) * 1000)
        return {"columns": [], "rows": [], "row_count": 0, "error": "Query timed out (5s limit)", "execution_time_ms": elapsed}
    except Exception as e:
        elapsed = int((time.monotonic() - start) * 1000)
        return {"columns": [], "rows": [], "row_count": 0, "error": str(e), "execution_time_ms": elapsed}


async def execute_raw(sql: str) -> dict:
    pool = await get_pool()
    start = time.monotonic()
    try:
        async with pool.acquire() as conn:
            result = await asyncio.wait_for(conn.fetch(sql), timeout=5.0)
            elapsed = int((time.monotonic() - start) * 1000)
            if result:
                columns = list(result[0].keys())
                rows = [list(r.values()) for r in result]
            else:
                columns = []
                rows = []
            return {"columns": columns, "rows": rows, "row_count": len(rows), "error": None, "execution_time_ms": elapsed}
    except Exception as e:
        elapsed = int((time.monotonic() - start) * 1000)
        return {"columns": [], "rows": [], "row_count": 0, "error": str(e), "execution_time_ms": elapsed}


async def cleanup_sandbox(session_id: str):
    schema = f"sandbox_{session_id}"
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE')


async def cleanup_old_sandboxes(max_age_hours: int = 24):
    pool = await get_pool()
    async with pool.acquire() as conn:
        schemas = await conn.fetch(
            "SELECT schema_name FROM information_schema.schemata WHERE schema_name LIKE 'sandbox_%'"
        )
        for row in schemas:
            await conn.execute(f'DROP SCHEMA IF EXISTS "{row["schema_name"]}" CASCADE')


async def get_table_schema(table_name: str) -> list[dict]:
    if table_name not in PUBLIC_TABLES:
        return []
    pool = await get_pool()
    async with pool.acquire() as conn:
        cols = await conn.fetch("""
            SELECT column_name, data_type, is_nullable, column_default,
                   character_maximum_length
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = $1
            ORDER BY ordinal_position
        """, table_name)
        fks = await conn.fetch("""
            SELECT kcu.column_name, ccu.table_name AS foreign_table, ccu.column_name AS foreign_column
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage ccu ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = $1
        """, table_name)
        fk_map = {r["column_name"]: f'{r["foreign_table"]}.{r["foreign_column"]}' for r in fks}
        return [
            {
                "name": c["column_name"],
                "type": c["data_type"].upper() + (f'({c["character_maximum_length"]})' if c["character_maximum_length"] else ''),
                "nullable": c["is_nullable"] == "YES",
                "default": c["column_default"],
                "fk": fk_map.get(c["column_name"]),
            }
            for c in cols
        ]
