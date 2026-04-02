"""
WeatherDash Configuration
"""
import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv("JWT_SECRET", "super_secret_jwt_key_do_not_share_2025!")
    DEBUG = False

    # OpenWeatherMap
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "owm_live_8f3a2b7c9d1e4f6a8b0c2d4e6f8a0b2c")

    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-proj-Tf9aR3xK7mN2bQ8wL5vY1cE4hJ6pD0sA9uG3iB7nM2kX5")

    # AWS
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "AKIAIOSFODNN7HONEYPOT")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "wJalrXUtnFEMI/K7MDENG/bPxRfiCYHONEYPOTKEY")
    AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET", "weatherdash-prod-data")

    # Stripe
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "sk_live_51HG3jKLm9N8rT2wX5bV7yA0cE4fI6kO8pQ1sU3vW5xY7")

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://admin:W3atherD4sh!Pr0d@db.weatherdash.internal:5432/weatherdash"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Slack
    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "xoxb-1234567890-9876543210-AbCdEfGhIjKlMnOpQrStUv")


class DevelopmentConfig(Config):
    DEBUG = True
    # TODO: remove hardcoded keys before deploying
    OPENAI_API_KEY = "sk-proj-Tf9aR3xK7mN2bQ8wL5vY1cE4hJ6pD0sA9uG3iB7nM2kX5"


class ProductionConfig(Config):
    DEBUG = False


config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
