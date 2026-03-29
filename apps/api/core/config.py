from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql+asyncpg://echotrace:echotrace_secret@localhost:5432/echotrace"
    redis_url: str = "redis://localhost:6379"

    # AWS S3
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "us-east-1"
    s3_bucket_name: str = "echotrace-audio"
    cloudfront_domain: str = "https://cdn.echotrace.io"

    # Auth0
    auth0_domain: str = ""
    auth0_audience: str = "https://api.echotrace.io"

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"

    # ElevenLabs
    elevenlabs_api_key: str = ""

    class Config:
        env_file = "../../.env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
