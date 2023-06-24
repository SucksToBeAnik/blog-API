## Header
from fastapi import APIRouter, Depends, Path, Query
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models.auth import User
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from sqlalchemy.exc import SQLAlchemyError
from typing import Annotated
from exceptions import (
    authorization_exception_handler,
    item_not_found_exception_handler,
    unique_item_exception_hnadler,
)
from jose import jwt, JWTError
from datetime import timedelta, datetime
import config
import os

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={403: {"response": "You are not authorized"}},
)
## End of header


# START OF LOGIC
class LocalUser(BaseModel):
    username: str = Field(max_length=50)
    password: str
    email: str
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    is_ative: bool = Field(default=True)

    class Config:
        schema_extra = {
            "example": {
                "username": "test",
                "password": "test12345",
                "email": "test@gmail.com",
                "first_name": "test",
                "last_name": "test",
                "is_active": True,
            }
        }


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")


def get_hashed_password(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db):
    user_model = db.query(User).filter(User.username == username).first()
    if not user_model:
        raise authorization_exception_handler()
    if not verify_password(password, user_model.hashed_password):
        raise authorization_exception_handler()
    return user_model


def create_access_token(
    username: str, user_id: int, token_expires_in: timedelta | None = None
):
    to_encode = {"sub": username, "id": user_id}

    if token_expires_in:
        expire_time = datetime.utcnow() + token_expires_in
    else:
        expire_time = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire_time})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# END OF LOGIC


# BODY
async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise authorization_exception_handler()
        return {"username": username, "id": user_id}
    except JWTError:
        raise authorization_exception_handler()


@router.get("/user")
async def get_all_users(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
    skip: Annotated[int, Query(gte=0)] = 0,
    limit: Annotated[int, Query(gt=0)] = 10,
):
    user_models = db.query(User).offset(skip).limit(limit).all()

    if not user_models:
        return {"response": "No registered users"}
    return user_models


@router.post("/user")
async def register_user(local_user: LocalUser, db: Session = Depends(get_db)):
    user_model = User()
    existing_user_model = (
        db.query(User).filter(User.username == local_user.username).first()
    )
    print(existing_user_model)
    if existing_user_model:
        raise unique_item_exception_hnadler()

    user_model.username = local_user.username
    user_model.email = local_user.email
    user_model.first_name = local_user.first_name
    user_model.last_name = local_user.last_name
    user_model.is_ative = local_user.is_ative
    user_model.hashed_password = get_hashed_password(local_user.password)

    try:
        db.add(user_model)
        db.commit()
    except SQLAlchemyError as e:
        return {"error": "There was an error while registering. Please try again!"}

    return {"response": "Registration was successful!"}





@router.put("/user")
async def update_user(
    local_user: LocalUser,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_id = user.get('id')
    user_model = db.query(User).filter(User.id == user_id).first()
    if user_model is None:
        raise item_not_found_exception_handler()
    
    user_model.username = local_user.username
    user_model.email = local_user.email
    user_model.first_name = local_user.first_name
    user_model.last_name = local_user.last_name
    user_model.is_ative = local_user.is_ative
    user_model.hashed_password = get_hashed_password(local_user.password)

    try:
        db.add(user_model)
        db.commit()
    except SQLAlchemyError as e:
        return {"error": "There was an error while registering. Please try again!"}
    return {
        'response':'User updated successfully'
    }




@router.delete("/user/{user_id}")
async def delete_user(
    user_id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)
):
    user_model = db.query(User).filter(User.id == user_id).first()
    if user_model is None:
        raise item_not_found_exception_handler()
    db.query(User).filter(User.id == user_id).delete()
    db.commit()

    return {"response": "User deleted!"}


# END OF BODY

##  FOOTER


@router.post("/user/token")
async def login_for_access_token(
    login_form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user_model = authenticate_user(login_form.username, login_form.password, db)
    token = login_for_access_token(
        user_model.username, user_model.id, token_expires_in=timedelta(minutes=20)
    )

    return {"token": token}
