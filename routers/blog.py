from fastapi import APIRouter
from exceptions import item_not_found_exception


router = APIRouter(
    prefix='/blog',
    tags=['Blog'],
    responses={403:{'message':'You are not authorized to perform this action.'}}
)

@router.get('/')
async def get_all_blogs():
    pass
    
    