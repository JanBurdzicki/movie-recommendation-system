import uvicorn
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status

from controller.main import router as main_router
from controller.movies import router as movies_router
from controller.ratings import router as ratings_router
from controller.recommendations import router as recommendations_router
from controller.users import router as users_router

app = FastAPI()

app.include_router(main_router, prefix="")
app.include_router(movies_router, prefix="/movies")
app.include_router(ratings_router, prefix="/ratings")
app.include_router(recommendations_router, prefix="/recommendations")
app.include_router(users_router, prefix="/users")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
