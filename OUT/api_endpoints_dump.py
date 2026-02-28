import json
from django.urls import URLPattern, URLResolver, get_resolver

rows = []


def walk(patterns, prefix=""):
    for p in patterns:
        if isinstance(p, URLResolver):
            walk(p.url_patterns, prefix + str(p.pattern))
            continue
        if not isinstance(p, URLPattern):
            continue
        path = prefix + str(p.pattern)
        if "api" not in path:
            continue
        callback = p.callback
        cls = getattr(callback, "cls", None)
        actions = getattr(callback, "actions", None)

        serializer = None
        permissions = []
        view_name = cls.__name__ if cls else getattr(callback, "__name__", str(callback))

        if cls is not None:
            serializer = getattr(cls, "serializer_class", None)
            serializer = serializer.__name__ if serializer else None
            permissions = [perm.__name__ for perm in getattr(cls, "permission_classes", [])]

        if actions:
            for method, action in actions.items():
                rows.append(
                    {
                        "path": "/" + path,
                        "method": method.upper(),
                        "view": view_name,
                        "action": action,
                        "serializer": serializer,
                        "permissions": permissions,
                    }
                )
        else:
            method_names = []
            if cls is not None:
                for m in ["get", "post", "put", "patch", "delete"]:
                    fn = getattr(cls, m, None)
                    if callable(fn):
                        method_names.append(m.upper())
            else:
                method_names = ["ANY"]
            for method in method_names or ["ANY"]:
                rows.append(
                    {
                        "path": "/" + path,
                        "method": method,
                        "view": view_name,
                        "action": "custom/standard",
                        "serializer": serializer,
                        "permissions": permissions,
                    }
                )

walk(get_resolver().url_patterns)

seen = set()
out = []
for r in sorted(rows, key=lambda x: (x["path"], x["method"], x["view"])):
    key = (r["path"], r["method"], r["view"], r["action"])
    if key in seen:
        continue
    seen.add(key)
    out.append(r)

print(json.dumps(out, indent=2))
