from fastapi import FastAPI
from app.api.routes import router as api_router
from dotenv import load_dotenv
import os

# ✅ Load environment variables from .env file
load_dotenv()

# Optional: Debug check (comment out or remove in production)
#print("Loaded OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="AI Autopilot Agentic System")

# Include all API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "API is running"}

