from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "1234567890"

DEBUG = True

ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_WHITELIST = ["http://localhost:5173"]

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    #
    "corsheaders",
    "django_extensions",
    #
    "app.core",
    "app.board",
    "app.solver",
    "app.socket",
]

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

ROOT_URLCONF = "dj_config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI_APPLICATION = "dj_config.wsgi.application"
ASGI_APPLICATION = "dj_config.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": ["redis://:guest@127.0.0.1:6379/1"],
        },
    },
}

"""Logging settings ->"""
DJANGO_LOG_LEVEL = "WARNING"
APP_LOG_LVL = "DEBUG"
LOGS_DIR = "logs"

FILE_DJANGO = BASE_DIR / LOGS_DIR / "django_logging.log"
FILE_APPS_LOGS = BASE_DIR / LOGS_DIR / "apps_logging.log"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} | {asctime} | {filename} ({lineno}) | {funcName} | {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} | {funcName} ({lineno}) | {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file_django": {
            "level": DJANGO_LOG_LEVEL,
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "midnight",
            "interval": 1,
            "backupCount": 10,
            "filename": FILE_DJANGO,
            "formatter": "verbose",
        },
        "file": {
            "level": APP_LOG_LVL,
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "midnight",
            "interval": 1,
            "backupCount": 10,
            "filename": FILE_APPS_LOGS,
            "formatter": "verbose",
        },
        "console": {
            "level": APP_LOG_LVL,
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django": {
            "handlers": ("file_django", "console"),
            "level": DJANGO_LOG_LEVEL,
            "propagate": True,
        },
        "app": {
            "handlers": ("file", "console"),
            "level": APP_LOG_LVL,
            "propagate": True,
        },
        "dj_config": {
            "handlers": ("file", "console"),
            "level": APP_LOG_LVL,
            "propagate": True,
        },
        "help_scripts": {
            "handlers": ("file", "console"),
            "level": APP_LOG_LVL,
            "propagate": True,
        },
    },
}
"""<- Logging settings"""

"""sentry.io config ->"""
USE_SENTRY = False
"""< - sentry.io config"""
