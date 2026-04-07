from fastapi import FastAPI, Depends, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routers import auth, houses, search
from app.db.database import init_db

# Define the lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # initialize tables (development); production should use migrations
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:5173"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(houses.router, prefix="/houses", tags=["houses"])
app.include_router(search.router, prefix="/search", tags=["search"])

@app.get("/")
def root():
    return {"status": "ok"}
