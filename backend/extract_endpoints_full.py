import os
import django
import sys
import inspect
from django.urls import get_resolver
from django.urls.resolvers import URLPattern, URLResolver

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
os.environ.setdefault('SECRET_KEY', 'test')
django.setup()

def get_view_name(callback):
    if hasattr(callback, '__name__'):
        return callback.__name__
    elif hasattr(callback, '__class__'):
        return callback.__class__.__name__
    return str(callback)

def get_view_module(callback):
    if hasattr(callback, '__module__'):
        return callback.__module__
    return "Unknown"

def extract_urls(urlpatterns, prefix=''):
    urls = []
    for pattern in urlpatterns:
        if isinstance(pattern, URLResolver):
            new_prefix = prefix + str(pattern.pattern)
            urls.extend(extract_urls(pattern.url_patterns, new_prefix))
        elif isinstance(pattern, URLPattern):
            url_str = f"/{prefix}{pattern.pattern}"
            view_name = get_view_name(pattern.callback)
            module_name = get_view_module(pattern.callback)

            # Simple API path detection
            if url_str.startswith('/api/'):
                kind = "API"
            elif url_str.startswith('/admin/'):
                kind = "ADMIN"
            else:
                kind = "WEB"

            urls.append(f"{kind} | {url_str} | {module_name}.{view_name} | {pattern.name}")
    return urls

urls = extract_urls(get_resolver().url_patterns)
for url in sorted(urls):
    print(url)
