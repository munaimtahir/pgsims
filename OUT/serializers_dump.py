import importlib
import inspect
import json
import pkgutil
from rest_framework import serializers
import sims

records = []


def example_for_field(field):
    name = field.__class__.__name__
    mapping = {
        "CharField": "string",
        "EmailField": "user@example.com",
        "SlugField": "sample-slug",
        "URLField": "https://example.com",
        "IntegerField": 1,
        "FloatField": 1.5,
        "DecimalField": "10.00",
        "BooleanField": True,
        "DateField": "2026-01-01",
        "DateTimeField": "2026-01-01T00:00:00Z",
        "ChoiceField": "choice_value",
        "UUIDField": "00000000-0000-0000-0000-000000000000",
        "ListField": [],
    }
    if name in mapping:
        return mapping[name]
    if isinstance(field, serializers.PrimaryKeyRelatedField):
        return 1
    if isinstance(field, serializers.ListSerializer):
        return []
    if isinstance(field, serializers.BaseSerializer):
        return {}
    return "value"


for _, app_name, _ in pkgutil.iter_modules(sims.__path__):
    for mod_suffix in ["serializers", "api_serializers"]:
        mod_name = f"sims.{app_name}.{mod_suffix}"
        try:
            module = importlib.import_module(mod_name)
        except Exception:
            continue

        for name, cls in inspect.getmembers(module, inspect.isclass):
            if not issubclass(cls, serializers.BaseSerializer):
                continue
            if cls in {
                serializers.BaseSerializer,
                serializers.Serializer,
                serializers.ModelSerializer,
                serializers.ListSerializer,
                serializers.HyperlinkedModelSerializer,
            }:
                continue
            if not cls.__module__.startswith(mod_name):
                continue

            record = {
                "module": mod_name,
                "name": name,
                "type": cls.__bases__[0].__name__ if cls.__bases__ else "Serializer",
                "fields": [],
                "example": {},
                "error": None,
            }
            try:
                inst = cls()
                fields = inst.get_fields()
                for fname, field in fields.items():
                    info = {
                        "name": fname,
                        "type": field.__class__.__name__,
                        "required": bool(getattr(field, "required", False)),
                        "read_only": bool(getattr(field, "read_only", False)),
                        "write_only": bool(getattr(field, "write_only", False)),
                        "allow_null": bool(getattr(field, "allow_null", False)),
                    }
                    record["fields"].append(info)
                    if not info["read_only"]:
                        record["example"][fname] = example_for_field(field)
            except Exception as exc:
                record["error"] = str(exc)

            records.append(record)

records.sort(key=lambda x: (x["module"], x["name"]))
print(json.dumps(records, indent=2))
