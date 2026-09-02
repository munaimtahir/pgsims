#!/usr/bin/env python
"""
Preload Attendance Data Script for SIMS

This script creates sample attendance data for demonstration:
- Creates attendance records for PG students
- Shows attendance calculations and eligibility
- Useful for testing attendance reporting features

Usage:
    python scripts/preload_attendance_data.py

Or via manage.py:
    python manage.py shell < scripts/preload_attendance_data.py
"""

import os
import sys
import django
from datetime import date, timedelta
from pathlib import Path
import random

# Setup Django environment
if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(project_root))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sims_project.settings")
    django.setup()

from django.contrib.auth import get_user_model
from django.db import transaction
from sims.attendance.models import AttendanceRecord, AttendanceSession
from sims.rotations.models import Rotation

User = get_user_model()


@transaction.atomic
def create_attendance_data():
    """Create sample attendance data for PG students"""
    print("=" * 70)
    print("Creating Sample Attendance Data")
    print("=" * 70)
    print(f"Using demo attendance rate: {DEFAULT_ATTENDANCE_RATE * 100:.0f}%")
    
    # Get PG students
    students = User.objects.filter(role='pg', is_archived=False)
    
    if not students.exists():
        print("✗ No PG students found. Please run preload_demo_data.py first.")
        return
    
    print(f"Found {students.count()} PG students")
    
    # Get ongoing rotations
    rotations = Rotation.objects.filter(
        status__in=['ongoing', 'planned'],
        start_date__lte=date.today(),
        end_date__gte=date.today()
    )
    
    if not rotations.exists():
        print("✗ No active rotations found.")
        return
    
    print(f"Found {rotations.count()} active rotations")
    
    attendance_records = []
    sessions_created = 0
    
    # Create attendance sessions and records for each rotation
    for rotation in rotations:
        print(f"\nProcessing rotation: {rotation.pg.username} - {rotation.department.name}")
        
        # Calculate number of days in rotation so far
        start_date = max(rotation.start_date, date.today() - timedelta(days=60))
        days_elapsed = (date.today() - start_date).days
        
        # Create weekly sessions
        session_count = min(days_elapsed // 7, 8)  # Max 8 weeks of data
        
        for week in range(session_count):
            session_date = start_date + timedelta(weeks=week)
            
            # Create session
            session_data = {
                'rotation': rotation,
                'date': session_date,
                'session_type': 'clinical',
                'duration_hours': 40,  # Weekly hours
                'conducted_by': rotation.supervisor,
            }
            
            session, created = AttendanceSession.objects.get_or_create(
                rotation=rotation,
                date=session_date,
                defaults=session_data
            )
            
            if created:
                sessions_created += 1
            
            # Create attendance record with realistic attendance pattern
            # 75-95% attendance randomly
            is_present = random.random() < 0.85  # 85% attendance rate
            
            record_data = {
                'session': session,
                'student': rotation.pg,
                'is_present': is_present,
                'marked_by': rotation.supervisor,
                'marked_at': session_date,
                'remarks': 'On duty' if is_present else 'Medical leave' if random.random() < 0.5 else 'Absent',
            }
            
            record, created = AttendanceRecord.objects.get_or_create(
                session=session,
                student=rotation.pg,
                defaults=record_data
            )
            
            if created:
                attendance_records.append(record)
    
    print("\n" + "=" * 70)
    print("✓ Attendance data created successfully!")
    print("=" * 70)
    print("\nSummary:")
    print(f"  • Students with attendance: {students.count()}")
    print(f"  • Sessions created: {sessions_created}")
    print(f"  • Attendance records: {len(attendance_records)}")
    
    # Calculate and display attendance percentages
    print("\nAttendance Summary by Student:")
    for student in students:
        total_sessions = AttendanceRecord.objects.filter(student=student).count()
        present_sessions = AttendanceRecord.objects.filter(
            student=student,
            is_present=True
        ).count()
        
        if total_sessions > 0:
            percentage = (present_sessions / total_sessions) * 100
            status = "✓ Eligible" if percentage >= 75 else "✗ Not Eligible"
            print(f"  • {student.username}: {present_sessions}/{total_sessions} ({percentage:.1f}%) {status}")
    
    print("=" * 70)


def create_sample_csv():
    """Create a sample CSV file for attendance import"""
    csv_path = Path(__file__).resolve().parent.parent / 'attendance_sample.csv'
    
    # Get a sample student
    student = User.objects.filter(role='pg', is_archived=False).first()
    
    if not student:
        print("No students found for CSV sample")
        return
    
    # Get student's rotation
    rotation = Rotation.objects.filter(pg=student, status='ongoing').first()
    
    if not rotation:
        print("No ongoing rotation found for CSV sample")
        return
    
    csv_content = """Date,Student_Username,Session_Type,Is_Present,Duration_Hours,Remarks
{},{},clinical,True,8,Regular attendance
{},{},clinical,True,8,Regular attendance
{},{},clinical,False,0,Sick leave
{},{},clinical,True,8,Regular attendance
{},{},clinical,True,8,Regular attendance
""".format(
        date.today() - timedelta(days=20), student.username,
        date.today() - timedelta(days=15), student.username,
        date.today() - timedelta(days=10), student.username,
        date.today() - timedelta(days=5), student.username,
        date.today(), student.username,
    )
    
    with open(csv_path, 'w') as f:
        f.write(csv_content)
    
    print(f"\n✓ Sample CSV created at: {csv_path}")
    print("  You can use this CSV as a template for bulk attendance import.")


def main():
    """Main function"""
    try:
        create_attendance_data()
        create_sample_csv()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
