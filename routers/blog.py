from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from exceptions import item_not_found_exception_handler
from database import get_db


router = APIRouter(
    prefix="/blog",
    tags=["Blog"],
    responses={403: {"response": "You are not authorized to perform this action."}},
)





@router.get("/")
async def get_all_blogs(db: Session = Depends(get_db)):
    pass
