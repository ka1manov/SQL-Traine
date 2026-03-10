from pydantic import BaseModel


class ExecuteRequest(BaseModel):
    sql: str
    session_id: str | None = None


class ExecuteResponse(BaseModel):
    columns: list[str]
    rows: list[list]
    row_count: int
    error: str | None = None
    execution_time_ms: int = 0


class CheckRequest(BaseModel):
    sql: str
    session_id: str | None = None


class DiffResult(BaseModel):
    match_pct: float
    matching_rows: list[list]
    missing_rows: list[list]
    extra_rows: list[list]
    expected_columns: list[str]
    actual_columns: list[str]
    order_correct: bool = True
    column_order_match: bool = True


class CheckResponse(BaseModel):
    correct: bool
    match_pct: float
    diff: DiffResult | None = None
    actual: ExecuteResponse | None = None
    expected: ExecuteResponse | None = None
    error: str | None = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    category: str
    difficulty: str
    hint: str | None = None
    tables: list[str]


class TaskDetail(TaskOut):
    solution_sql: str | None = None
    explanation: str | None = None


class ProgressEntry(BaseModel):
    task_id: int
    solved: bool
    best_match_pct: float
    attempts: int


class MockStartRequest(BaseModel):
    difficulty: str | None = None


class MockSession(BaseModel):
    session_id: str
    task_ids: list[int]
    time_limit: int
    started_at: str | None = None


class MockEndRequest(BaseModel):
    session_id: str
    results: list[dict]


class MockResult(BaseModel):
    total_score: float
    tasks_solved: int
    total_tasks: int
    time_used: int | None = None
    details: list[dict]


# Auth
class AuthRequest(BaseModel):
    username: str


class AuthResponse(BaseModel):
    user_id: int
    username: str
    token: str


# History
class HistoryEntry(BaseModel):
    id: int
    sql_text: str
    execution_time_ms: int | None
    row_count: int
    had_error: bool
    created_at: str


# Bookmarks
class BookmarkRequest(BaseModel):
    task_id: int


# Flashcard spaced repetition
class FlashcardReview(BaseModel):
    card_id: int
    quality: int  # 0-5 SM-2 scale


class FlashcardState(BaseModel):
    card_id: int
    ease_factor: float
    interval_days: int
    repetitions: int
    next_review: str


# Streak
class StreakDay(BaseModel):
    date: str
    task_id: int


# Leaderboard
class LeaderboardEntry(BaseModel):
    username: str
    tasks_solved: int
    total_attempts: int
    avg_match_pct: float


# SQL Format
class FormatRequest(BaseModel):
    sql: str


class FormatResponse(BaseModel):
    formatted: str


# Column schema
class ColumnInfo(BaseModel):
    name: str
    type: str
    nullable: bool
    default: str | None
    fk: str | None
