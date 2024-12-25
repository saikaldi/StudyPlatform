import os
from pathlib import Path
from decouple import config
from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    'drf_spectacular',
    "apps.users",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = "staticfiles"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

AUTH_USER_MODEL = "users.User"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),                              # Время жизни access токена
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),                                # Время жизни refresh токена
    "ROTATE_REFRESH_TOKENS": False,                                             # Ротация refresh токенов при каждом запросе
    "BLACKLIST_AFTER_ROTATION": True,                                           # Добавлять старые refresh токены в blacklist (если включена ротация)
    "UPDATE_LAST_LOGIN": False,                                                 # Обновлять поле last_login при получении токена
    "ALGORITHM": "HS256",                                                       # Алгоритм шифрования токена
    "SIGNING_KEY": SECRET_KEY,                                                  # Секретный ключ для подписания токенов
    "VERIFYING_KEY": None,                                                      # Публичный ключ (если используется асимметричное шифрование)
    "AUDIENCE": None,                                                           # Аудитория токена
    "ISSUER": None,                                                             # Издатель токена
    "AUTH_HEADER_TYPES": ("Bearer",),                                           # Префикс авторизации в заголовке (например, "Bearer <token>")
    "USER_ID_FIELD": "id",                                                      # Поле для идентификации пользователя
    "USER_ID_CLAIM": "user_id",                                                 # Поле внутри токена, в котором хранится user_id
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),     # Классы токенов
    "TOKEN_TYPE_CLAIM": "token_type",                                           # Поле в токене, указывающее его тип
    "JTI_CLAIM": "jti",                                                         # Уникальный идентификатор токена
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),                             # Время жизни скользящих токенов (если используется SlidingToken)
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),                        # Время жизни refresh для SlidingToken
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "aktanarynov566@gmail.com"
EMAIL_HOST_PASSWORD = "zelt flio uuax zgnk"

ADMIN_EMAIL = "aktanarynov566@gmail.com"

SPECTACULAR_SETTINGS = {
    'TITLE': 'API для ОРТ',
    'DESCRIPTION': 'API для ОРТ',
    'VERSION': '1.0.0',
}
