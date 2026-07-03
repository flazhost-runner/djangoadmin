import environ
from pathlib import Path
environ.Env.read_env(Path(__file__).resolve().parent.parent.parent / '.env.development')
from .base import *  # noqa: F401, F403
from .base import env  # noqa: F401
DEBUG = True
ALLOWED_HOSTS = ['*']
