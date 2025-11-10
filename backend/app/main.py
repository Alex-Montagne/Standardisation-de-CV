from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.api.api_router import router as api_router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Standardisation de CV")

@app.get("/", response_class=HTMLResponse)
def root():
    return """
        <h1>Bienvenue sur l’API de standardisation de CV</h1>
        """

app.include_router(api_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

app.mount("/outputs", StaticFiles(directory=OUTPUTS_DIR), name="outputs")