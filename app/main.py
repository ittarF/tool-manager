from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, SessionLocal, Base
from sqlalchemy.orm import Session
from .routers import tool_lookup, tool_usage, tools
from .init_tools import initialize_tools

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Tool-Manager",
    description="An application designed to store tool information and implementations",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tool_lookup.router, tags=["Tool Lookup"])
app.include_router(tool_usage.router, tags=["Tool Usage"])
app.include_router(tools.router, tags=["Tools"])

@app.get("/")
async def root():
    return {"message": "Welcome to Tool-Manager API"}

@app.on_event("startup")
async def startup_event():
    """Initialize tools on startup"""
    initialize_tools() 