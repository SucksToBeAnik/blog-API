from fastapi import HTTPException, status

def item_not_found_exception_handler():
    response = HTTPException(
        status_code= status.HTTP_404_NOT_FOUND,
        detail= {'error':f"Item not found"}
    )
    
    return response

def authorization_exception_handler():
    response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={'error':'Invalid username or password'}
    )
    return response
    
def unique_item_exception_hnadler():
    response = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail={'error':'Username already taken!'}
    )
    return response






