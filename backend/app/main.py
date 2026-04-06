from fastapi import FastAPI, Depends, APIRouter, HTTPException
from contextlib import asynccontextmanager
from app.routers import auth
from app.db.database import init_db

# Define the lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # initialize tables (development); production should use migrations
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def root():
    return {"status": "ok"}
