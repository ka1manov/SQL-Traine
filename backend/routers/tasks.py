from dataclasses import asdict

from fastapi import APIRouter, HTTPException, Request
from models.schemas import TaskOut, TaskDetail, CheckRequest, CheckResponse, ColumnInfo
from data.tasks import TASKS, TASKS_BY_ID
from data.flashcards import FLASHCARDS
from data.assignments import ASSIGNMENTS
from data.learning_paths import LEARNING_PATHS
from services.sandbox import create_sandbox, execute_in_sandbox, execute_raw, PUBLIC_TABLES, get_table_schema
from services.diff import compute_diff

router = APIRouter(prefix="/api", tags=["tasks"])


@router.get("/tasks", response_model=list[TaskOut])
async def list_tasks(category: str | None = None, difficulty: str | None = None):
    result = TASKS
    if category:
        result = [t for t in result if t.category == category]
    if difficulty:
        result = [t for t in result if t.difficulty == difficulty]
    return [TaskOut(**{k: v for k, v in t.__dict__.items() if k != 'solution_sql'}) for t in result]


@router.get("/tasks/meta")
async def tasks_meta():
    """Return categories, difficulties, and counts for dynamic frontend use."""
    categories = {}
    difficulties = {}
    for t in TASKS:
        categories.setdefault(t.category, []).append(t.id)
        difficulties.setdefault(t.difficulty, []).append(t.id)
    return {"total": len(TASKS), "categories": categories, "difficulties": difficulties}


@router.get("/tasks/{task_id}", response_model=TaskDetail)
async def get_task(task_id: int):
    task = TASKS_BY_ID.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskDetail(**task.__dict__)


@router.post("/tasks/{task_id}/check", response_model=CheckResponse)
async def check_task(task_id: int, req: CheckRequest):
    task = TASKS_BY_ID.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session_id = await create_sandbox(req.session_id)
    actual = await execute_in_sandbox(session_id, req.sql)
    if actual.get("error"):
        return CheckResponse(
            correct=False, match_pct=0,
            error=actual["error"],
            actual=actual, expected=None, diff=None,
        )

    expected = await execute_raw(task.solution_sql)
    diff = compute_diff(expected, actual)

    return CheckResponse(
        correct=diff["match_pct"] == 100 and diff["order_correct"],
        match_pct=diff["match_pct"],
        diff=diff,
        actual=actual,
        expected=expected,
        error=None,
    )


@router.get("/flashcards")
async def list_flashcards():
    return [asdict(f) for f in FLASHCARDS]


@router.get("/assignments")
async def list_assignments():
    return [
        {
            "id": a.id,
            "title": a.title,
            "company": a.company,
            "description": a.description,
            "tables": a.tables,
            "steps": [s.__dict__ for s in a.steps],
        }
        for a in ASSIGNMENTS
    ]


@router.get("/learning-paths")
async def list_learning_paths():
    return [asdict(lp) for lp in LEARNING_PATHS]


@router.get("/tables")
async def list_tables():
    return {"tables": PUBLIC_TABLES}


@router.get("/tables/{table_name}")
async def get_table_data(table_name: str, limit: int = 100, offset: int = 0):
    if table_name not in PUBLIC_TABLES:
        raise HTTPException(status_code=404, detail="Table not found")
    capped_limit = min(max(limit, 1), 500)
    capped_offset = max(offset, 0)
    result = await execute_raw(
        f'SELECT * FROM public."{table_name}" LIMIT {capped_limit} OFFSET {capped_offset}'
    )
    count_result = await execute_raw(f'SELECT COUNT(*) AS total FROM public."{table_name}"')
    total = count_result["rows"][0][0] if count_result["rows"] else 0
    result["total_rows"] = total
    return result


@router.get("/tables/{table_name}/schema", response_model=list[ColumnInfo])
async def get_table_schema_endpoint(table_name: str):
    if table_name not in PUBLIC_TABLES:
        raise HTTPException(status_code=404, detail="Table not found")
    schema = await get_table_schema(table_name)
    return schema
