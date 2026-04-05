from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.database import init_db
from app.routers import houses, auth

app = FastAPI(title="house_finder_bot API")

# Allow local frontend (Expo web) and common dev origins. Narrow in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:19006", "http://127.0.0.1:19006", "http://localhost:19000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(houses.router, prefix="/houses", tags=["houses"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])


@app.on_event("startup")
async def startup_event():
    # initialize tables (development); production should use migrations
    init_db()


@app.get("/")
def root():
    return {"status": "ok"}
