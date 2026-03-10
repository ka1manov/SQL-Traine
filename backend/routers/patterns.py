from dataclasses import asdict

from fastapi import APIRouter, HTTPException
from data.patterns import PATTERNS, PATTERNS_BY_ID, PATTERN_CATEGORIES

router = APIRouter(prefix="/api", tags=["patterns"])


@router.get("/patterns")
async def list_patterns(category: str | None = None):
    result = PATTERNS
    if category:
        result = [p for p in result if p.category == category]
    return [asdict(p) for p in result]


@router.get("/patterns/categories")
async def get_categories():
    return PATTERN_CATEGORIES


@router.get("/patterns/{pattern_id}")
async def get_pattern(pattern_id: int):
    p = PATTERNS_BY_ID.get(pattern_id)
    if not p:
        raise HTTPException(status_code=404, detail="Pattern not found")
    return asdict(p)
