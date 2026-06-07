from fastapi import FastAPI, Form, HTTPException, File, UploadFile, Path, Depends

import httpx
from sqlalchemy import select
from .schemas import PostCreate, PostResponse, UserCreate, UserRead, UserUpdate
from app.db import Post, User, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from app.images import imagekit
import shutil
import os
import uuid
import tempfile

from app.user import auth_backend, fastapi_users, current_active_user

async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# app terhubung dengan auth backend dari fastapi-users
# dan otomatis membuat route untuk register, login, dll di bawah dengan prefix untuk routenya /auth/jwt
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"]
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"]
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"]
)

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    user : User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)   
):
    temp_file_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        upload_result = imagekit.files.upload(
            file=open(temp_file_path, "rb"),
            file_name=file.filename,
            tags=["backend-upload"]
        )

        if upload_result and hasattr(upload_result, 'url'):
            post = Post(
                user_id=user.id,
                caption=caption,
                url=upload_result.url,
                file_type="video" if file.content_type.startswith("video/") else "image",
                file_name=upload_result.name
            )
            # id otomate generate dengan session.add() dan session.commit() 
            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await file.close()
        
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except PermissionError:
                # Jika Windows masih keras kepala mengunci file, kita biarkan OS yang membersihkannya nanti
                # Ini mengamankan agar aplikasi tidak crash di fase finally
                pass

@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    result = await session.execute(select(User))
    users = {row[0] for row in result.all()}
    user_dict = {u.id : u.email for u in users}

    posts_data=[]

    for post in posts:
        posts_data.append(
            {
                "id": post.id,
                "user_id": str(post.user_id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat(),
                "is_owner": post.user_id == user.id,
                "email" : user_dict.get(post.user_id, "Unknown")
            }
        )
    
    return ("posts", posts_data)

@app.delete("/posts/{post_id}")
async def delete_post(
    post_id: str = Path(..., description="ID of the post to delete"),
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    try :
        post_uuid = uuid.UUID(post_id)
        
        result = await session.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalar_one_or_none()
        
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        if post.user_id != user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this post")

        await session.delete(post)
        await session.commit()

        return {"success": True, "message": "Post deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))