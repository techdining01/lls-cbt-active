from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database.database import init_database
from app.services.licensing.api import router as license_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure all tables exist on startup
    init_database()
    yield


app = FastAPI(
    title="LLS-CBT Licensing API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(license_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "success": True,
        "service": "LLS-CBT Licensing API",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}