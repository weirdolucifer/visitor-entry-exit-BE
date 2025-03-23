import os

from . import common


class Settings(common.Settings):
    """Class for django settings development mode"""

    DEBUG = True
    ENVIRONMENT_CODE = os.environ.get("ENVIRONMENT_CODE", "dev")
    ALLOWED_HOSTS = ["*"]
