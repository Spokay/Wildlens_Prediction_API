from fastapi import HTTPException
from starlette import status


def extract_api_key(auth_header):
    try:
        return auth_header.split("Key ")[1]
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
