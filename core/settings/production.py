from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
# python manage.py runserver --insecure

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]

INSTALLED_APPS += []

MIDDLEWARE += []

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = { 
    "default": { 
        "ENGINE": "django.db.backends.postgresql_psycopg2", 
        "NAME": config("SQL_DATABASE"), 
        "USER": config("SQL_USER"), 
        "PASSWORD": config("SQL_PASSWORD"), 
        "HOST": config("SQL_HOST"), 
        "PORT": config("SQL_PORT"), 
        "ATOMIC_REQUESTS": True,
    }
} 

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# LOGGING
LOGGING = { 
    "version": 1, 
    "disable_existing_loggers": True, 
    "formatters": {
        'verbose': { 
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}', 
            'style': '{', 
        },
    }, 
    "handlers": {
        'file': { 
            'class': 'logging.FileHandler', 
            "formatter": "verbose", 
            'filename': './debug.log', 
            'level': 'WARNING', 
        }, 
    }, 
    "loggers": { 
        "django": { 
            "handlers": ['file'],  
            "level": config("DJANGO_LOG_LEVEL", "WARNING"), 
            'propagate': True, 
        }, 
    }, 
}
