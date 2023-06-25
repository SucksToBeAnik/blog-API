from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session
from exceptions import item_not_found_exception_handler
from database import get_db
from routers.auth import get_current_user
from models.blog import Blog
from pydantic import BaseModel, Field
from sqlalchemy.exc import SQLAlchemyError



router = APIRouter(
    prefix="/blog",
    tags=["Blog"],
    responses={403: {"response": "You are not authorized to perform this action."}},
)


class LocalBlog(BaseModel):
    title: str = Field(max_length=50)
    body: str

    class Config:
        schema_extra = {"example": {"title": "Test", "body": "This is a test body"}}


@router.get("/")
async def get_all_blogs(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
    skip: int = Query(default=0,ge=0),
    limit: int = Query(default=10,gt=0)
):
    blog_models = (
        db.query(Blog)
        .filter(Blog.owner_id == user.get("id"))
        .offset(skip)
        .limit(limit)
        .all()
    )

    return blog_models


@router.get("/{blog_id}")
async def get_single_blog(
    blog_id: int= Path(...,gt=0),
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    blog_model = (
        db.query(Blog)
        .filter(Blog.id == blog_id)
        .filter(Blog.owner_id == user.get("id"))
        .first()
    )
    
    if not blog_model:
        raise item_not_found_exception_handler()

    return blog_model


@router.post("/")
async def create_blog(
    local_blog: LocalBlog,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    blog_model = Blog()

    blog_model.title = local_blog.title
    blog_model.body = local_blog.body
    blog_model.owner_id = user.get("id")

    try:
        db.add(blog_model)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    return {"response": "Blog was created!"}


@router.put("/update/{blog_id}")
def update_blog(
    local_blog: LocalBlog,
    blog_id: int= Path(...,gt=0),
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    blog_model = (
        db.query(Blog)
        .filter(Blog.id == blog_id)
        .filter(Blog.owner_id == user.get("id"))
        .first()
    )
    
    if not blog_model:
        raise item_not_found_exception_handler()
    blog_model.title = local_blog.title
    blog_model.body = local_blog.body
    blog_model.owner_id = user.get("id")

    try:
        db.add(blog_model)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    return {"response": "Blog was updated!"}

@router.delete('/delete/{blog_id}')
async def delete_blog(
    blog_id: int= Path(gt=0),
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    blog_model = (
        db.query(Blog)
        .filter(Blog.id == blog_id)
        .filter(Blog.owner_id == user.get("id"))
        .first()
    )
    
    if not blog_model:
        raise item_not_found_exception_handler()
    
    try:
        db.query(Blog).filter(Blog.id == blog_id).filter(Blog.owner_id == user.get('id')).delete()
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    
    return {
        'response':'Blog was deleted'
    }

    
    
    
