from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Docling API"
    upload_dir: str = "/tmp/uploads"

    class Config:
        env_file = ".env"

settings = Settings()
