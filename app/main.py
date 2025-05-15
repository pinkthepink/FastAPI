from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

from app.database.mongodb import lifespan
from app.api.api_router import api_router
from app.core.config import settings
from app.core.errors import PetshopException

# Create FastAPI app with lifespan
app = FastAPI(
    title="Petshop API",
    description="API for pet shop management system",
    version="1.0.0",
    lifespan=lifespan,  # Use lifespan for MongoDB connection management
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Global exception handler
@app.exception_handler(PetshopException)
async def petshop_exception_handler(request: Request, exc: PetshopException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "details": exc.details},
    )

# Include all routes
app.include_router(api_router, prefix="/api")

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Petshop API is running. Access /docs for documentation."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=settings.PORT, 
        reload=settings.ENVIRONMENT == "development"
    )