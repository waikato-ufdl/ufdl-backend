"""
Django settings for ufdl project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import datetime
import os

import psycopg2.extensions

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# Auto-generate a secret key (and a JWT signing key)
# Based on: https://stackoverflow.com/a/4674143
try:
    from .secret import SECRET_KEY, JWT_SIGNING_KEY, DEBUG, ALLOWED_HOSTS
except ImportError:
    from django.core.management.utils import get_random_secret_key
    current_dir = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(current_dir, "secret.py"), "w") as file:
        file.write(f"SECRET_KEY='{get_random_secret_key()}'\n")
        file.write(f"JWT_SIGNING_KEY='{get_random_secret_key()}'\n")
        file.write(f"DEBUG=True\n")
        file.write(f"ALLOWED_HOSTS=['*']\n")
    from .secret import SECRET_KEY, JWT_SIGNING_KEY
    
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    
    ALLOWED_HOSTS = [
        "localhost",
        "127.0.0.1",
    ]


# Application definition

INSTALLED_APPS = [
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'ufdl.core_app',
    'ufdl.image_classification_app',
    'ufdl.object_detection_app',
    'ufdl.speech_app',
    'ufdl.image_segmentation_app',
    'simple_django_teams',
    'ufdl.html_client_app'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True  # TODO: Is it wise to allow all?

ROOT_URLCONF = 'ufdl.api_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ufdl.api_site.wsgi.application'
ASGI_APPLICATION = 'ufdl.api_site.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                (
                    os.environ.get('UFDL_REDIS_HOST', 'localhost'),
                    int(os.environ.get('UFDL_REDIS_PORT', '6379'))
                )
            ],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

def gen_database_name() -> str:
    """
    Generates the name of the database.
    """
    return os.path.join(BASE_DIR, 'db.sqlite3')


#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': gen_database_name()
#    }
#}

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'OPTIONS': {
#            'read_default_file': '/Scratch/ufdl-backend/config/my.cnf',
#        },
#    }
#}

DATABASES = {
    'default': {
        'NAME': 'ufdl',
        'ENGINE': 'django.db.backends.postgresql',
        'USER': os.environ.get('UFDL_POSTGRESQL_USER', 'ufdl'),
        'PASSWORD': os.environ.get('UFDL_POSTGRESQL_PASSWORD', ''),
        'HOST': os.environ.get('UFDL_POSTGRESQL_HOST', 'localhost'),
        'OPTIONS': {
            'client_encoding': 'UTF8'
        },
    }
}

AUTH_USER_MODEL = 'ufdl-core.User'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-NZ'

TIME_ZONE = 'NZ'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Email
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_PORT = 587
#EMAIL_USE_TLS = True
#EMAIL_HOST_USER = "user@gmail.com"
#EMAIL_HOST_PASSWORD = "password"
#DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# Configure the authentication in Django Rest Framework to be JWT
# http://www.django-rest-framework.org/
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    # Access for 1 hour, refresh for 1 day
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(hours=8),

    # Must sign in for new refresh token, instead of receiving one automatically
    # on refresh
    "ROTATE_REFRESH_TOKENS": False,

    # Symmetric signing, provides authentication but not privacy
    "ALGORITHM": "HS256",
    "SIGNING_KEY": JWT_SIGNING_KEY,
    "VERIFYING_KEY": None,  # Not used for symmetric (HMAC) signing

    # Asymmetric signing/encryption
    # "ALGORITHM": "RS256",
    # "SIGNING_KEY": MY_PRIVATE_KEY,
    # "VERIFYING_KEY": MY_PUBLIC_KEY,

    # Field names
    "USER_ID_CLAIM": "upk",  # For compactness, default "user_id"
    "TOKEN_TYPE_CLAIM": "jtt"  # For compactness, default "token_type"
}

UFDL = {
    # File-system backend
    "FILESYSTEM_BACKEND": "ufdl.core_app.backend.filesystem.LocalDiskBackend",

    "LOCAL_DISK_FILE_DIRECTORY": "fs"
}

UFDL_HTML_CLIENT = {
    "SERVE_CLIENT": True
}

APPEND_SLASH = False
