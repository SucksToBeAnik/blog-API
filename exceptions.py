from fastapi import HTTPException, status

def item_not_found_exception(title, info):
    exception = HTTPException(
        status_code= status.HTTP_404_NOT_FOUND,
        detail= f"{title} with this information {info} do not exist"
    )
    
    return exception


