from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://edutrack:edutrack@db:5432/edutrack"

    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 720

    cors_origins: str = "http://localhost:3000"

    admin_email: str = "admin@edutrack.io"
    admin_password: str = "admin123"

    # Default academic thresholds (used to seed the settings table).
    pass_mark: float = 10.0
    risk_average: float = 10.0
    high_absence_rate: float = 0.15
    performance_drop: float = 3.0
    expected_hours: float = 200.0  # reference total hours used for the absence rate

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
