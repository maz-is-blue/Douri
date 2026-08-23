"""
Django settings for the Douri asbl website.

Local dev uses SQLite and local-disk media out of the box. For production,
set DATABASE_URL (see .env.example) to swap in Postgres via dj-database-url,
and swap MEDIA storage for S3/Cloudinary (see README "Going to production").
"""

from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY', default='django-insecure-change-me-in-production')
DEBUG = env('DEBUG', default=True)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'ckeditor',

    'core',
    'projects',
    'interviews',
    'agenda',
    'people',
    'social',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'douri.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'douri.wsgi.application'

# Database
# Local dev: SQLite (see db.sqlite3 below).
# Production: set DATABASE_URL, e.g. postgres://user:pass@host:5432/dbname
DATABASES = {
    'default': env.db('DATABASE_URL', default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Luxembourg'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Local dev serves uploads from disk. Swap for S3 (django-storages) or
# Cloudinary in production — see README "Going to production".
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/admin/login/'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Basic',
        'height': 300,
        'width': 'auto',
    },
}

# ---------------------------------------------------------------------------
# django-jazzmin — themed admin ("the dashboard")
# ---------------------------------------------------------------------------
JAZZMIN_SETTINGS = {
    'site_title': 'Douri Dashboard',
    'site_header': 'Douri',
    'site_brand': 'Douri Dashboard',
    'site_logo': None,
    'welcome_sign': 'Welcome to the Douri content dashboard',
    'copyright': 'Douri asbl',
    'search_model': ['projects.Project', 'interviews.Interview'],
    'topmenu_links': [
        {'name': 'View website', 'url': '/', 'new_window': True},
    ],
    'show_sidebar': True,
    'navigation_expanded': True,
    'order_with_respect_to': [
        'core', 'projects', 'interviews', 'agenda', 'people', 'social', 'auth',
    ],
    'icons': {
        'auth': 'fas fa-users-cog',
        'auth.user': 'fas fa-user',
        'auth.Group': 'fas fa-users',
        'core.HeroSlide': 'fas fa-images',
        'core.SiteSettings': 'fas fa-cog',
        'core.FormSubmission': 'fas fa-inbox',
        'projects.Project': 'fas fa-hands-helping',
        'projects.Workshop': 'fas fa-paint-brush',
        'interviews.Interview': 'fas fa-comment-dots',
        'agenda.AgendaFeatured': 'fas fa-star',
        'agenda.AgendaRecurring': 'fas fa-calendar-alt',
        'people.TeamMember': 'fas fa-id-badge',
        'people.Partner': 'fas fa-handshake',
        'social.InstagramPost': 'fab fa-instagram',
    },
    'custom_css': 'css/admin-douri.css',
}

JAZZMIN_UI_TWEAKS = {
    'navbar_small_text': False,
    'footer_small_text': False,
    'body_small_text': False,
    'brand_small_text': False,
    'brand_colour': 'navbar-info',
    'accent': 'accent-info',
    'navbar': 'navbar-white navbar-light',
    'no_navbar_border': False,
    'sidebar': 'sidebar-light-info',
    'sidebar_nav_small_text': False,
    'sidebar_disable_expand': False,
    'sidebar_nav_child_indent': True,
    'sidebar_nav_compact_style': False,
    'sidebar_nav_legacy_style': False,
    'sidebar_nav_flat_style': False,
    'theme': 'default',
    'button_classes': {
        'primary': 'btn-outline-info',
        'secondary': 'btn-outline-secondary',
        'info': 'btn-info',
        'warning': 'btn-warning',
        'danger': 'btn-danger',
        'success': 'btn-success',
    },
}
