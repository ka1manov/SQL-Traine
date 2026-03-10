from dataclasses import asdict

from fastapi import APIRouter, HTTPException, Request
from models.schemas import CheckRequest, CheckResponse, InterviewProgressEntry
from data.interview_questions import INTERVIEW_QUESTIONS, QUESTIONS_BY_ID
from services.sandbox import create_sandbox, execute_in_sandbox, execute_raw
from services.diff import compute_diff
from services.dependencies import get_user_id, require_user_id
from db.connection import get_pool

router = APIRouter(prefix="/api", tags=["interview"])


@router.get("/interview-questions")
async def list_questions(company: str | None = None, pattern: str | None = None, difficulty: str | None = None):
    result = INTERVIEW_QUESTIONS
    if company:
        result = [q for q in result if company in q.company_tags]
    if pattern:
        result = [q for q in result if q.pattern == pattern]
    if difficulty:
        result = [q for q in result if q.difficulty == difficulty]
    return [
        {
            "id": q.id,
            "title": q.title,
            "description": q.description,
            "company_tags": q.company_tags,
            "pattern": q.pattern,
            "difficulty": q.difficulty,
            "tables": q.tables,
            "hint": q.hint,
        }
        for q in result
    ]


@router.get("/interview-questions/meta")
async def questions_meta():
    companies: dict[str, int] = {}
    patterns: dict[str, int] = {}
    for q in INTERVIEW_QUESTIONS:
        for c in q.company_tags:
            companies[c] = companies.get(c, 0) + 1
        patterns[q.pattern] = patterns.get(q.pattern, 0) + 1
    return {
        "total": len(INTERVIEW_QUESTIONS),
        "companies": companies,
        "patterns": patterns,
    }


@router.get("/interview-questions/progress")
async def get_interview_progress(request: Request):
    user_id = await get_user_id(request)
    if not user_id:
        return []
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT question_id, solved, best_match_pct, attempts FROM interview_progress WHERE user_id = $1",
            user_id,
        )
        return [dict(r) for r in rows]


@router.post("/interview-questions/progress")
async def update_interview_progress(entry: InterviewProgressEntry, request: Request):
    user_id = await require_user_id(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        existing = await conn.fetchrow(
            "SELECT * FROM interview_progress WHERE user_id = $1 AND question_id = $2",
            user_id, entry.question_id,
        )
        if existing:
            await conn.execute("""
                UPDATE interview_progress
                SET attempts = attempts + 1,
                    best_match_pct = GREATEST(best_match_pct, $3),
                    solved = solved OR $4,
                    last_attempt_at = NOW()
                WHERE user_id = $1 AND question_id = $2
            """, user_id, entry.question_id, entry.best_match_pct, entry.solved)
        else:
            await conn.execute("""
                INSERT INTO interview_progress (user_id, question_id, solved, best_match_pct, attempts)
                VALUES ($1, $2, $3, $4, $5)
            """, user_id, entry.question_id, entry.solved, entry.best_match_pct, entry.attempts)

        row = await conn.fetchrow(
            "SELECT question_id, solved, best_match_pct, attempts FROM interview_progress WHERE user_id = $1 AND question_id = $2",
            user_id, entry.question_id,
        )
        return dict(row)


@router.get("/interview-questions/{question_id}")
async def get_question(question_id: int):
    q = QUESTIONS_BY_ID.get(question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return asdict(q)


@router.post("/interview-questions/{question_id}/check", response_model=CheckResponse)
async def check_question(question_id: int, req: CheckRequest):
    q = QUESTIONS_BY_ID.get(question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")

    session_id = await create_sandbox(req.session_id)
    actual = await execute_in_sandbox(session_id, req.sql)
    if actual.get("error"):
        return CheckResponse(
            correct=False, match_pct=0,
            error=actual["error"],
            actual=actual, expected=None, diff=None,
        )

    expected = await execute_raw(q.solution_sql)
    diff = compute_diff(expected, actual)

    return CheckResponse(
        correct=diff["match_pct"] == 100 and diff["order_correct"],
        match_pct=diff["match_pct"],
        diff=diff,
        actual=actual,
        expected=expected,
        error=None,
    )
