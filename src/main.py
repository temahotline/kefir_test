import uvicorn

from fastapi import FastAPI, APIRouter

from src.users.routers.auth_router import auth_router
from src.users.routers.private_router import private_router
from src.users.routers.users_router import users_router
from src.exception_handlers import (
    custom_400_exception_handler,
    custom_401_403_404_exception_handler,
    custom_422_exception_handler,
    internal_server_error_handler,
)


app = FastAPI(title="kefir_test")


main_api_router = APIRouter()
main_api_router.include_router(
    auth_router, prefix="", tags=["auth"]
)
main_api_router.include_router(
    private_router, prefix="/private", tags=["private"]
)
main_api_router.include_router(
    users_router, prefix="/users", tags=["users"])
app.include_router(main_api_router)
app.add_exception_handler(400, custom_400_exception_handler)
app.add_exception_handler(401, custom_401_403_404_exception_handler)
app.add_exception_handler(403, custom_401_403_404_exception_handler)
app.add_exception_handler(404, custom_401_403_404_exception_handler)
app.add_exception_handler(422, custom_422_exception_handler)
app.add_exception_handler(500, internal_server_error_handler)


if __name__ == "__main__":
    uvicorn.run(app, host="db", port=8000)
