import os
import django
import sys
from django.urls import get_resolver

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
os.environ.setdefault('SECRET_KEY', 'test')
django.setup()

def extract_urls(urlpatterns, prefix=''):
    urls = []
    for pattern in urlpatterns:
        if hasattr(pattern, 'url_patterns'):
            urls.extend(extract_urls(pattern.url_patterns, prefix + str(pattern.pattern)))
        else:
            urls.append(prefix + str(pattern.pattern))
    return urls

urls = extract_urls(get_resolver().url_patterns)
for url in sorted(urls):
    print(f"/{url}")
