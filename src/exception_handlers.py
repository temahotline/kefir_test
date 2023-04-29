from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette import status


async def custom_400_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.status_code, "message": exc.detail},
    )


async def custom_401_403_404_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


async def custom_422_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": [{"code": exc.status_code, "message": exc.detail}]},
    )


async def internal_server_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Что-то пошло не так, мы уже исправляем эту ошибку",
        },
    )
