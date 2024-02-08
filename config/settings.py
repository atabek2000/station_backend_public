import os
from pathlib import Path
import environ
from datetime import timedelta

# настройки environ
root = environ.Path(__file__) - 2
env = environ.Env()
environ.Env.read_env(env.str(root(), '.env'))

# основная директория
BASE_DIR = Path(__file__).resolve().parent.parent

AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend', 'users.backends.AuthBackend',]
#
SECRET_KEY = env.str('SECRET_KEY')

DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.str('ALLOWED_HOSTS', default='127.0.0.1').split(' ')


# base packages
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
# packages
INSTALLED_APPS += [
    'rest_framework',  # drf
    'django_filters',  # filters for django
    'corsheaders',  # module for accessing headers
    'djoser',  # for registration, login and logout
    'phonenumber_field',  # for validating phone numbers
    'django_cleanup.apps.CleanupConfig',  # deleting files from server when is deleted from db
    'admin_extra_buttons',

    'users.apps.UsersConfig',
    'api.apps.ApiConfig',
    'common.apps.CommonConfig',
    'shop.apps.ShopConfig',
    'order.apps.OrderConfig',
    'subscribes.apps.SubscribesConfig',
]
# after all apps
INSTALLED_APPS += [
    'drf_spectacular',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'crum.CurrentRequestUserMiddleware',
]


ROOT_URLCONF = 'config.urls'


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


WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('DB_NAME', 'station'),
        'USER': env.str('DB_USER', 'postgres'),
        'PASSWORD': env.str('DB_PASSWORD'),
        'HOST': env.str('DB_HOST'),
        'PORT': env.int('DB_PORT'),
    },
    'extra': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


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

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


###########################
# DJANGO REST FRAMEWORK
###########################
REST_FRAMEWORK = {
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',),

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],

    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FileUploadParser',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'common.pagination.BasePagination',
}


######################
# LOCALIZATION
######################
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Asia/Almaty'
USE_I18N = True
USE_TZ = True


######################
# STATIC AND MEDIA
######################
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
# python manage.py collectstatic


###########################
# CORS HEADERS
###########################
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ['*']
CSRF_COOKIE_SECURE = False


######################
# DRF SPECTACULAR
######################
SPECTACULAR_SETTINGS = {
    'TITLE': 'STATION',
        'DESCRIPTION': 'Api for STATION',
    'VERSION': '1.0.0',

    'SERVE_PERMISSIONS': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    'SERVE_AUTHENTICATION': [
        'rest_framework.authentication.BasicAuthentication',
    ],

    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        "displayOperationId": True,
        # "syntaxHighlight.active": True,
        # "syntaxHighlight.theme": "arta",
        # "defaultModelsExpandDepth": -1,
        # "displayRequestDuration": True,
        # "filter": True,
        # "requestSnippetsEnabled": True,
    },

    'COMPONENT_SPLIT_REQUEST': True,
    'SORT_OPERATIONS': False,

    # 'ENABLE_DJANGO_DEPLOY_CHECK': False,
    # 'DISABLE_ERRORS_AND_WARNINGS': True,
}

#######################
# DJOSER
#######################
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': False,
    'SERIALIZERS': {},
}

#######################
# JWT
#######################
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=7),
}

#######################
# JAZZMIN
#######################
JAZZMIN_SETTINGS = {
    "site_title": "Station",
    "site_header": "Station",
    "welcome_sign": "Welcome to the Station",
    "copyright": "Station",
}