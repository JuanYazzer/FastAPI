from fastapi import FastAPI, HTTPException, Path
import httpx
from .schemas import PostCreate, PostResponse
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

app = FastAPI()

text_posts = {
    1 :{
        "title" : "First Post",
        "content" : "This is the first post"
    },
    2 :{
        "title" : "Second Post",
        "content" : "This is the second post"
    },
    3 :{
        "title" : "Third Post",
        "content" : "This is the third post"
    },
    4 :{
        "title" : "Fourth Post",
        "content" : "This is the fourth post"
    },
    5 :{
        "title" : "Fifth Post",
        "content" : "This is the fifth post"
    }
}

@app.get("/posts")
def get_all_posts():
    return text_posts

@app.get("/posts")
def get_limit_posts(limit: int = Path(..., description="The number of posts to return", gt=0)):
    return list(text_posts.values())[:limit]

@app.get("/posts/{post_id}")
def get_post(post_id: int):
    if post_id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")

    return text_posts[post_id]

@app.post("/posts")
def create_post(post: PostCreate) -> PostResponse:
    post_id = max(text_posts.keys()) + 1
    text_posts[post_id] = post
    return text_posts[post_id]

