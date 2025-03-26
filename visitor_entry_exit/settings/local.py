import os
from pathlib import Path

from . import common


class Settings(common.Settings):
    """Class for django settings local mode"""

    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    DOTENV = ".env"
    DEBUG = True
    ENVIRONMENT_CODE = os.environ.get("ENVIRONMENT_CODE", "dev")
    ALLOWED_HOSTS = ["*"]
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
    MEDIA_URL = '/media/'
    LOGGING = {}
