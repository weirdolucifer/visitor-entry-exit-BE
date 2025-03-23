import os
from pathlib import Path

import dotenv

dotenv.load_dotenv(dotenv_path="envs/test.env")

from . import common


class Settings(common.Settings):
    """Class for django settings testing mode"""

    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    ENVIRONMENT_CODE = os.environ.get("ENVIRONMENT_CODE", "Test")
    ALLOWED_HOSTS = ["*"]
    DEBUG = False

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "visitor_test_db",
            "USER": os.environ.get("POSTGRES_USER"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
            "HOST": os.environ.get("POSTGRES_HOST") or "localhost",
            "PORT": os.environ.get("POSTGRES_PORT") or "5432",
        },
    }

    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        },
    }

    LOGGING = {}
