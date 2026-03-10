import os
import uuid
import jwt
from db.connection import get_pool

JWT_SECRET = os.getenv("JWT_SECRET", "sql-trainer-dev-secret")


def create_token(user_id: int, username: str) -> str:
    return jwt.encode({"user_id": user_id, "username": username}, JWT_SECRET, algorithm="HS256")


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return None


async def get_or_create_user(username: str) -> dict:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT id, username, token FROM app_users WHERE username = $1", username)
        if row:
            return {"user_id": row["id"], "username": row["username"], "token": create_token(row["id"], row["username"])}
        token = uuid.uuid4().hex
        row = await conn.fetchrow(
            "INSERT INTO app_users (username, token) VALUES ($1, $2) RETURNING id, username",
            username, token,
        )
        return {"user_id": row["id"], "username": row["username"], "token": create_token(row["id"], row["username"])}


async def get_user_id_from_token(token: str) -> int | None:
    payload = decode_token(token)
    if not payload:
        return None
    return payload.get("user_id")
