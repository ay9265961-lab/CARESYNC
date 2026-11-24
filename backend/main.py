
from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database setup
from backend.database import Base, engine

# Import models so all database tables are registered
from backend import models

# Import API routers
from backend.routers import auth
from backend.routers import medicines
from backend.routers import appointments
from backend.routers import family
from backend.routers import approvals
from backend.routers import activity


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="CARESYNC",
    description=(
        "AI-powered elderly assistance "
        "and family coordination platform."
    ),
    version="0.1.0"
)


# Register API routers
app.include_router(auth.router)
app.include_router(medicines.router)
app.include_router(appointments.router)
app.include_router(family.router)
app.include_router(approvals.router)
app.include_router(activity.router)


@app.get("/", tags=["General"])
def home():
    return {
        "application": "CARESYNC",
        "message": "Welcome to CARESYNC!",
        "status": "running"
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "application": "CARESYNC",
        "status": "healthy"
    }
