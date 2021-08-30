"""
Django settings for lssrp_core project.
Generated by 'django-admin startproject' using Django 3.1.2.
For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import environ
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

root = environ.Path(__file__) - 2

# Fetch env vars
os.environ.setdefault("ENV_FILE", root(".env"))
env = environ.Env(DEBUG=(bool, False))
if os.path.isfile(os.environ["ENV_FILE"]):
    env.read_env(os.environ["ENV_FILE"])

SECRET_KEY = env("SECRET_KEY", default="NOT_NEEDED_FOR_DOCKER_BUILDS")
ALLOWED_HOSTS = env("ALLOWED_HOSTS", default=[])

# Application definition

INSTALLED_APPS = [
    "lssrp_app",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tailwind",
    "tinymce",
    "django_bleach",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.cache.FetchFromCacheMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "lssrp_core.urls"

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

TAILWIND_APP_NAME = "lssrp_app"
NPM_BIN_PATH = env("NPM_BIN_PATH", default=r"C:\Program Files\nodejs\npm.cmd")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "lssrp_core.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {"default": env.db() if env("DATABASE_URL", default=None) else {}}

#############
#           #
#   DEBUG   #
#           #
#############

DEBUG = env("DEBUG", default=True)

# Debug Toolbar
if DEBUG:
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    INSTALLED_APPS += ["debug_toolbar"]

INTERNAL_IPS = [
    "127.0.0.1",
] + env.list("DEBUG_IPS", default=[])


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "sl-SI"
TIME_ZONE = "CET"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_ROOT = root(env("STATIC_DIR", default="../static"))
MEDIA_ROOT = root(env("MEDIA_DIR", default="../media"))

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # other finders..
]

SESSION_COOKIE_SAMESITE = env("SESSION_COOKIE_SAMESITE", default="None")
SESSION_COOKIE_SECURE = env("SESSION_COOKIE_SECURE", default=True)
CSRF_COOKIE_SAMESITE = env("CSRF_COOKIE_SAMESITE", default="None")
CSRF_COOKIE_SECURE = env("CSRF_COOKIE_SECURE", default=True)
CSRF_USE_SESSIONS = env("CSRF_USE_SESSIONS", default=False)

LOGIN_URL = "/prijava"
LOGIN_REDIRECT_URL = "/"

DECORATIVE_EMAIL_DOMAIN = env("DECORATIVE_EMAIL_DOMAIN", default="los-santos.com")

# https://github.com/jazzband/django-tinymce/issues/333
TINYMCE_COMPRESSOR = env("TINYMCE_COMPRESSOR", default=True)
TINYMCE_DEFAULT_CONFIG = {
    "theme": "silver",
    "height": 500,
    "menubar": False,
    "plugins": "advlist,autolink,lists,link,image,charmap,print,preview,anchor,"
    "searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,paste,"
    "code,help,wordcount",
    "toolbar": "undo redo | formatselect | "
    "bold italic backcolor | alignleft aligncenter "
    "alignright alignjustify | bullist numlist outdent indent | "
    "removeformat | help",
    "suffix": ".min" if TINYMCE_COMPRESSOR else ""
}

BLEACH_ALLOWED_TAGS = [
    "span",
    "p",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "pre",
    "strong",
    "em",
    "li",
    "ul",
    "ol",
    "div",
    "br",
]
BLEACH_ALLOWED_ATTRIBUTES = {"*": ["style", "class"]}
BLEACH_ALLOWED_STYLES = [
    "background-color",
    "color",
    "text-align",
    "list-style-type",
    "padding-left",
    "padding-right",
]
