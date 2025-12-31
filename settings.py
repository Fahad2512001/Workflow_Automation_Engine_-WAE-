from pathlib import Path
import os

# -----------------------------
# BASE DIRECTORY
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# SECURITY
# -----------------------------
SECRET_KEY = 'your-secret-key'  # Replace in production
DEBUG = True
ALLOWED_HOSTS = []  # Add your domain in production

# -----------------------------
# INSTALLED APPS
# -----------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'core',  # your app
    'rest_framework',
]

# -----------------------------
# MIDDLEWARE
# -----------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -----------------------------
# URLS & WSGI
# -----------------------------
ROOT_URLCONF = 'workflow_engine.urls'
WSGI_APPLICATION = 'workflow_engine.wsgi.application'

# -----------------------------
# TEMPLATES
# -----------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Point to 'templates' folder; Django will find core/login.html automatically
        'DIRS': [os.path.join(BASE_DIR, 'core', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Required by auth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# -----------------------------
# DATABASE
# -----------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# -----------------------------
# PASSWORD VALIDATION (Development)
# -----------------------------
AUTH_PASSWORD_VALIDATORS = []

# -----------------------------
# INTERNATIONALIZATION
# -----------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# -----------------------------
# STATIC FILES
# -----------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'core', 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# -----------------------------
# MEDIA FILES
# -----------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# -----------------------------
# LOGIN / LOGOUT REDIRECTS
# -----------------------------
LOGIN_REDIRECT_URL = '/dashboard/'       # Redirect after login
LOGOUT_REDIRECT_URL = '/accounts/login/' # Redirect after logout

# -----------------------------
# DEFAULT AUTO FIELD
# -----------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
