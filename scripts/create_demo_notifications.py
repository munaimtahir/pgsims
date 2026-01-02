#!/usr/bin/env python
"""
Create Demo Notifications Script

This script creates sample in-app notifications for testing the notification system.

Usage:
    python scripts/create_demo_notifications.py
"""

import os
import sys
import django
from datetime import datetime, timedelta
from pathlib import Path

# Setup Django environment
if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(project_root))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sims_project.settings")
    django.setup()

from django.contrib.auth import get_user_model
from django.db import transaction
from sims.notifications.models import Notification
from sims.logbook.models import LogbookEntry
from sims.cases.models import ClinicalCase

User = get_user_model()


@transaction.atomic
def create_demo_notifications():
    """Create sample notifications for demo users"""
    print("=" * 70)
    print("Creating Demo Notifications")
    print("=" * 70)
    
    # Get users
    students = User.objects.filter(role='pg', is_archived=False)
    supervisors = User.objects.filter(role='supervisor', is_archived=False)
    
    if not students.exists() or not supervisors.exists():
        print("✗ No students or supervisors found. Run preload_demo_data.py first.")
        return
    
    notifications_created = 0
    
    # Create notifications for students (from supervisors)
    for student in students:
        try:
            User._meta.get_field('supervisor')
            supervisor = getattr(student, 'supervisor', None)
            if not supervisor:
                supervisor = supervisors.first()
        except Exception:
            supervisor = supervisors.first()
        
        # Notification 1: Logbook entry approved
        notification_data = {
            'recipient': student,
            'actor': supervisor,
            'verb': 'approved',
            'title': 'Logbook Entry Approved',
            'body': f'{supervisor.get_full_name()} has approved your recent logbook entry.',
            'channel': 'in_app',
            'metadata': {'type': 'logbook_approved'},
        }
        
        notification, created = Notification.objects.get_or_create(
            recipient=student,
            title=notification_data['title'],
            created_at__gte=datetime.now() - timedelta(days=1),
            defaults=notification_data
        )
        
        if created:
            notifications_created += 1
            print(f"✓ Created notification for {student.username}: Logbook approved")
        
        # Notification 2: New rotation assignment
        notification_data = {
            'recipient': student,
            'actor': supervisor,
            'verb': 'assigned',
            'title': 'New Rotation Assignment',
            'body': 'You have been assigned to a new rotation. Check your rotations page for details.',
            'channel': 'in_app',
            'metadata': {'type': 'rotation_assigned'},
            'created_at': datetime.now() - timedelta(hours=2),
        }
        
        notification, created = Notification.objects.get_or_create(
            recipient=student,
            title=notification_data['title'],
            created_at__gte=datetime.now() - timedelta(days=1),
            defaults=notification_data
        )
        
        if created:
            notifications_created += 1
            print(f"✓ Created notification for {student.username}: New rotation")
    
    # Create notifications for supervisors (from students)
    for supervisor in supervisors:
        assigned_students = User.objects.filter(supervisor=supervisor, role='pg', is_archived=False)
        
        if not assigned_students.exists():
            continue
            
        for student in assigned_students:
            # Notification 1: New logbook entry to review
            notification_data = {
                'recipient': supervisor,
                'actor': student,
                'verb': 'submitted',
                'title': 'New Logbook Entry to Review',
                'body': f'{student.get_full_name()} has submitted a new logbook entry for your review.',
                'channel': 'in_app',
                'metadata': {'type': 'logbook_review_needed'},
            }
            
            notification, created = Notification.objects.get_or_create(
                recipient=supervisor,
                actor=student,
                title=notification_data['title'],
                created_at__gte=datetime.now() - timedelta(days=1),
                defaults=notification_data
            )
            
            if created:
                notifications_created += 1
                print(f"✓ Created notification for {supervisor.username}: Review needed")
            
            # Notification 2: New clinical case submitted
            notification_data = {
                'recipient': supervisor,
                'actor': student,
                'verb': 'submitted',
                'title': 'New Clinical Case Submitted',
                'body': f'{student.get_full_name()} has submitted a new clinical case for review.',
                'channel': 'in_app',
                'metadata': {'type': 'case_review_needed'},
                'created_at': datetime.now() - timedelta(hours=4),
            }
            
            notification, created = Notification.objects.get_or_create(
                recipient=supervisor,
                actor=student,
                title=notification_data['title'],
                created_at__gte=datetime.now() - timedelta(days=1),
                defaults=notification_data
            )
            
            if created:
                notifications_created += 1
                print(f"✓ Created notification for {supervisor.username}: Case review")
    
    print("\n" + "=" * 70)
    print(f"✓ Created {notifications_created} demo notifications")
    print("=" * 70)
    print("\nNotification Summary:")
    for user in User.objects.filter(is_archived=False, role__in=['pg', 'supervisor']):
        count = Notification.objects.filter(recipient=user, read_at__isnull=True).count()
        print(f"  • {user.username}: {count} unread notifications")
    print("=" * 70)


def main():
    """Main function"""
    try:
        create_demo_notifications()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
