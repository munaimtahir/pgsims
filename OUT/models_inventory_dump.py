import json
import re
from django.apps import apps


def json_safe(value):
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    return str(value)


inventory = []
for model in sorted(apps.get_models(), key=lambda m: m._meta.label):
    meta = model._meta
    entry = {
        "label": meta.label,
        "app_label": meta.app_label,
        "model_name": meta.object_name,
        "db_table": meta.db_table,
        "fields": [],
        "relations": [],
        "status_fields": [],
    }

    for field in list(meta.concrete_fields) + list(meta.many_to_many):
        choices = getattr(field, "choices", None)
        remote_field = getattr(field, "remote_field", None)
        related_model = getattr(field, "related_model", None)

        info = {
            "name": field.name,
            "type": field.__class__.__name__,
            "null": bool(getattr(field, "null", False)),
            "blank": bool(getattr(field, "blank", False)),
            "has_choices": bool(choices),
            "primary_key": bool(getattr(field, "primary_key", False)),
            "unique": bool(getattr(field, "unique", False)),
            "is_relation": bool(getattr(field, "is_relation", False)),
        }
        if info["has_choices"]:
            info["choices_values"] = [json_safe(c[0]) for c in list(choices)]

        entry["fields"].append(info)

        if info["is_relation"]:
            entry["relations"].append(
                {
                    "field": field.name,
                    "relation_type": field.__class__.__name__,
                    "target": related_model._meta.label if related_model else None,
                    "related_name": getattr(remote_field, "related_name", None) if remote_field else None,
                }
            )

        if re.search(r"(status|state|phase|approval|review|submit|verify)", field.name, re.IGNORECASE):
            entry["status_fields"].append(
                {
                    "name": field.name,
                    "type": field.__class__.__name__,
                    "has_choices": bool(choices),
                    "choices_values": [json_safe(c[0]) for c in list(choices)] if choices else [],
                }
            )

    inventory.append(entry)

print(json.dumps(inventory, indent=2, sort_keys=True))
