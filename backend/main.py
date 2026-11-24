
from fastapi import FastAPI

app = FastAPI(
    title="CARESYNC",
    description="AI-powered elderly assistance and family coordination platform.",
    version="0.1.0"
)


@app.get("/", tags=["General"])
def home():
    return {
        "application": "CARESYNC",
        "message": "Welcome to CARESYNC!",
        "status": "under development"
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "application": "CARESYNC",
        "status": "healthy"
    }
