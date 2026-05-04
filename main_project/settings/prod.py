import os

from .base import *


def _split_csv(value):
    return [item.strip() for item in value.split(",") if item.strip()]


def _normalize_origin(value):
    value = value.strip()
    if not value:
        return ""
    if value.startswith("http://") or value.startswith("https://"):
        return value
    return f"https://{value}"


SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "unsafe-render-fallback-secret-key")
DEBUG = False

ALLOWED_HOSTS = ["*"]
SERVE_MEDIA = os.getenv("DJANGO_SERVE_MEDIA", "True").lower() == "true"
CONTACT_EMAIL_ENABLED = os.getenv("CONTACT_EMAIL_ENABLED", "False").lower() == "true"

_csrf_origins = [
    _normalize_origin(origin)
    for origin in _split_csv(os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", ""))
]
_csrf_origins.extend(
    _normalize_origin(host)
    for host in _split_csv(os.getenv("DJANGO_ALLOWED_HOSTS", ""))
)

render_hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME", "").strip()
if render_hostname:
    _csrf_origins.append(f"https://{render_hostname}")

CSRF_TRUSTED_ORIGINS = list(dict.fromkeys(origin for origin in _csrf_origins if origin))

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = os.getenv("DJANGO_SECURE_SSL_REDIRECT", "True").lower() == "true"
SECURE_HSTS_SECONDS = int(os.getenv("DJANGO_SECURE_HSTS_SECONDS", "31536000"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = (
    os.getenv("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", "True").lower() == "true"
)
SECURE_HSTS_PRELOAD = os.getenv("DJANGO_SECURE_HSTS_PRELOAD", "True").lower() == "true"
