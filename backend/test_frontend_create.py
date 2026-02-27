import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sims_project.settings")
django.setup()

from django.test import Client

from sims.users.models import User


def main():
    # Keep this as an ad-hoc local debug script; do not execute on import during test discovery.
    User.objects.filter(username="testadmin").delete()
    admin = User.objects.create_superuser("testadmin", "admin@test.com", "password", role="admin")

    admin_supervisor = User.objects.create_user(
        username="sup",
        password="password",
        role="supervisor",
        specialty="medicine",
        email="sup@sup.com",
        is_active=True,
    )

    client = Client(SERVER_NAME="localhost")
    client.force_login(admin)

    response = client.post(
        "/users/create/",
        {
            "username": "newpg",
            "email": "newpg@test.com",
            "first_name": "New",
            "last_name": "PG",
            "role": "pg",
            "specialty": "medicine",
            "year": "1",
            "password1": "StrongP@ss123",
            "password2": "StrongP@ss123",
            "supervisor_choice": admin_supervisor.id,
        },
    )
    print("POST /users/create/ Status Code:", response.status_code)
    if response.status_code == 200:
        for msg in response.context.get("messages", []):
            print(f"MESSAGE: {msg.message}")
    elif response.status_code == 302:
        print("Redirected to:", response.url)


if __name__ == "__main__":
    main()
