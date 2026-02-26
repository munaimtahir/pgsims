import os
import sys
import json
import inspect

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sims_project.settings")

import django
django.setup()

from django.urls import get_resolver, URLPattern, URLResolver
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin

def get_permissions(view_cls):
    if hasattr(view_cls, 'permission_classes'):
        return [p.__name__ for p in view_cls.permission_classes]
    return []

def extract_endpoints():
    resolver = get_resolver()
    endpoints = []
    
    def traverse(url_patterns, prefix=''):
        for pattern in url_patterns:
            if isinstance(pattern, URLResolver):
                traverse(pattern.url_patterns, prefix + str(pattern.pattern))
            elif isinstance(pattern, URLPattern):
                path = prefix + str(pattern.pattern)
                
                # Check if it's an API route (e.g. starts with api/)
                # Actually let's capture all, we will filter later or just output everything
                
                callback = pattern.callback
                cls = getattr(callback, 'view_class', None)
                actions = getattr(callback, 'actions', None)
                
                if cls:
                    perms = get_permissions(cls)
                    name = cls.__name__
                    
                    if actions:
                        # ViewSet
                        for method, action in actions.items():
                            action_func = getattr(cls, action, None)
                            serializer = None
                            if action_func and hasattr(action_func, 'kwargs') and 'serializer_class' in action_func.kwargs:
                                serializer = action_func.kwargs['serializer_class'].__name__
                            elif hasattr(cls, 'serializer_class') and cls.serializer_class:
                                serializer = cls.serializer_class.__name__
                                
                            endpoints.append({
                                'path': path,
                                'method': method.upper(),
                                'view': name,
                                'action': action,
                                'serializer': serializer,
                                'permissions': perms
                            })
                    else:
                        # Standard APIView
                        methods = [m.upper() for m in getattr(cls, 'http_method_names', [])] if hasattr(cls, 'http_method_names') else ['GET']
                        serializer = None
                        if hasattr(cls, 'serializer_class') and cls.serializer_class:
                           serializer = cls.serializer_class.__name__
                           
                        for m in methods:
                            if m not in ['OPTIONS', 'HEAD']:
                                endpoints.append({
                                    'path': path,
                                    'method': m,
                                    'view': name,
                                    'action': 'custom/standard',
                                    'serializer': serializer,
                                    'permissions': perms
                                })
                else:
                    # Function-based view or non-DRF view
                    endpoints.append({
                        'path': path,
                        'method': 'ANY',
                        'view': callback.__name__ if hasattr(callback, '__name__') else str(callback),
                        'action': 'func',
                        'serializer': None,
                        'permissions': []
                    })
                    
    traverse(resolver.url_patterns)
    
    return [e for e in endpoints if 'api/' in e['path'] or 'auth/' in e['path']]

if __name__ == '__main__':
    endpoints = extract_endpoints()
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'endpoints.json')
    with open(out_path, 'w') as f:
        json.dump(endpoints, f, indent=2)
    print(f"Saved {len(endpoints)} endpoints to {out_path}")
