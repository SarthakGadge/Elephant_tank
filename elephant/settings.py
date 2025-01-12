from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure--9%23cm^$lq*cf2rk9za5_%59q8$wf3&zajg$j*=r1-=+3$$pv"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
]
CORS_EXPOSE_HEADERS = [
    'Content-Type',
    'X-CSRFToken',
    'Authorization',
]

AWS_ACCESS_KEY_ID = 'AKIA47GB76VLKGOXHXSN'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'elephant-tank-bucket' 
AWS_S3_REGION_NAME = 'ap-south-1'

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'corsheaders',
    'rest_framework_simplejwt',
    'rest_framework',
    'userauth',
    'student',
    'storages',
    'investor',
    'funding',
    'admin_app',
    'form'
]


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"

# Custom folder paths for images, PDFs, and videos
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# S3 path for images
AWS_S3_IMAGE_UPLOAD_PATH = 'Images/'

# S3 path for PDFs
AWS_S3_PDF_UPLOAD_PATH = 'PDF/'

# S3 path for videos
AWS_S3_VIDEO_UPLOAD_PATH = 'Videos/'

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = "elephant.urls"

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

WSGI_APPLICATION = 'elephant.wsgi.application'

# AUTH_USER_MODEL = 'userauth.Student'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'elephant',  # Replace with your actual database name
#         'USER': 'root',  # Replace with your MySQL username
#         'PASSWORD': 'root',  # Replace with your MySQL password
#         'HOST': 'localhost',  # Use '127.0.0.1' if 'localhost' doesn't work
#         'PORT': '3306',  # The default MySQL port

#     }
# }

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = '/media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'elephant',
        'USER': 'dbmasteruser',
        'PASSWORD': 'database9014',
        'HOST': 'ls-f8259bafe38561c18d0d411f37aefbfabc0ff7bf.citdgny2wnek.ap-south-1.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

STATIC_URL = '/static/'

# In case you have custom directories for static files
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Assuming your static folder is in the root of the project
]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    # Set to True if you want to rotate refresh tokens on each login
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators


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

# Set a limit on the maximum file size (in bytes)
FILE_UPLOAD_MAX_MEMORY_SIZE = 31457280    # 50 MB (default: 2.5 MB)

# Increase the maximum request size (useful for large file uploads)
DATA_UPLOAD_MAX_MEMORY_SIZE = 31457280    # 50 MB (default: 2.5 MB)

FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

RAZORPAY_API_KEY = "rzp_test_sBeufim7qDE8nf"

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  # If using tokens
        # Optional for session-based auth
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Default permission class
    ],
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.hostinger.com"
EMAIL_PORT = 587  # Use 465 if using SSL
EMAIL_HOST_USER = "aa@thedatatechlabs.com"
EMAIL_HOST_PASSWORD = "Tdtl@2024#"
DEFAULT_FROM_EMAIL = "aa@thedatatechlabs.com"

# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.elephant-tank.com"  # Use the correct SMTP server address
# EMAIL_PORT = 587  # Standard for TLS (SSL is typically 465, but you seem to be using 587 for TLS)
# EMAIL_HOST_USER = "support@elephant-tank.com"  # Your Outlook email
# EMAIL_HOST_PASSWORD = "Tdtl@2024#"  # The password or app password for the Outlook account
# DEFAULT_FROM_EMAIL = "support@elephant-tank.com"  # Default sender email for your app

 


# Email: support@elephant-tank.com
# Password-:2024@Tdtl