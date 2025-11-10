from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    CLAUDE_API_KEY: str
    CLAUDE_MODEL: str = "claude-3-opus-20240229"
    TESSERACT_PATH: str = "C:/Program Files/Tesseract-OCR/tesseract.exe"

    class Config:
        env_file = ".env"

settings = Settings()