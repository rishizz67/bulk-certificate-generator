from fastapi import FastAPI

from app.database import init_db
from app.routes.jobs import router as jobs_router
from app.routes.certificates import router as certificates_router


init_db()


app = FastAPI(
    title="Bulk Certificate Generator API",
    description="API for generating certificates in bulk.",
    version="1.0.0"
)


app.include_router(jobs_router)
app.include_router(certificates_router)


@app.get("/")
def root():
    return {
        "message": "Bulk Certificate Generator API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }