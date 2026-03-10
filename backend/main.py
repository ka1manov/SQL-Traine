import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from db.connection import get_pool, close_pool
from services.sandbox import cleanup_old_sandboxes
from routers import execute, tasks, progress, mock, daily, history, bookmarks, streaks, leaderboard, format_sql, flashcard_review, auth
from data.templates import TEMPLATES


async def _periodic_cleanup():
    while True:
        await asyncio.sleep(3600)
        try:
            await cleanup_old_sandboxes()
        except Exception:
            pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    await get_pool()
    cleanup_task = asyncio.create_task(_periodic_cleanup())
    yield
    cleanup_task.cancel()
    await close_pool()


app = FastAPI(title="SQL Trainer", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(execute.router)
app.include_router(tasks.router)
app.include_router(progress.router)
app.include_router(mock.router)
app.include_router(daily.router)
app.include_router(history.router)
app.include_router(bookmarks.router)
app.include_router(streaks.router)
app.include_router(leaderboard.router)
app.include_router(format_sql.router)
app.include_router(flashcard_review.router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.get("/api/templates")
async def get_templates():
    return [t.__dict__ for t in TEMPLATES]
