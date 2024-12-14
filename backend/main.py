from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from core.config import settings
from api.v1.api import api_router
from db.init_db import init_db
from middleware.compliance import ComplianceMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add compliance middleware
app.add_middleware(ComplianceMiddleware)

# Mount frontend build directory
app.mount("/", StaticFiles(directory="frontend/build", html=True))

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 