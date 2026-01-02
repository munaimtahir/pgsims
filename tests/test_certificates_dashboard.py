#!/usr/bin/env python3
"""
Test script to debug certificate dashboard issues.

Created: 2025-01-27
Author: GitHub Copilot
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from sims.certificates.models import Certificate, CertificateType
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

def test_certificate_dashboard_data():
    """Test certificate dashboard data and queries"""
    print("=== Testing Certificate Dashboard ===")
    
    # Check users
    users = User.objects.all()
    admin_users = User.objects.filter(role='admin')
    supervisor_users = User.objects.filter(role='supervisor')
    pg_users = User.objects.filter(role='pg')
    
    print(f"Total users: {users.count()}")
    print(f"Admin users: {admin_users.count()}")
    print(f"Supervisor users: {supervisor_users.count()}")
    print(f"PG users: {pg_users.count()}")
    
    # Check certificate types
    cert_types = CertificateType.objects.all()
    print(f"\nCertificate types: {cert_types.count()}")
    for cert_type in cert_types[:3]:
        print(f"  - {cert_type.name}")
    
    # Check certificates
    certificates = Certificate.objects.all()
    print(f"\nTotal certificates: {certificates.count()}")
    
    if certificates.count() == 0:
        print("No certificates found. Creating test data...")
        
        # Create certificate types if they don't exist
        if cert_types.count() == 0:
            CertificateType.objects.create(
                name="BLS Certification",
                description="Basic Life Support Certification",
                is_required=True
            )
            CertificateType.objects.create(
                name="ACLS Certification", 
                description="Advanced Cardiac Life Support Certification",
                is_required=True
            )
            print("Created test certificate types")
        
        # Create test certificate if we have users
        if pg_users.exists():
            cert_type = CertificateType.objects.first()
            pg = pg_users.first()
            
            Certificate.objects.create(
                pg=pg,
                certificate_type=cert_type,
                title="Test BLS Certificate",
                issuing_organization="Test Medical Center",
                issue_date=timezone.now().date(),
                expiry_date=timezone.now().date() + timedelta(days=365),
                cme_points_earned=10,
                cpd_credits_earned=5,
                status='approved'
            )
            print("Created test certificate")
    
    # Test queries for different user roles
    for user in [admin_users.first(), supervisor_users.first(), pg_users.first()]:
        if user:
            print(f"\n--- Testing queries for {user.role}: {user.username} ---")
            
            try:
                if user.role == 'admin':
                    user_certificates = Certificate.objects.all()
                elif user.role == 'supervisor':
                    user_certificates = Certificate.objects.filter(pg__supervisor=user)
                elif user.role == 'pg':
                    user_certificates = Certificate.objects.filter(pg=user)
                else:
                    user_certificates = Certificate.objects.none()
                
                print(f"  Certificates accessible: {user_certificates.count()}")
                
                # Test statistics calculations
                today = timezone.now().date()
                stats = {
                    'total_certificates': user_certificates.count(),
                    'approved_certificates': user_certificates.filter(status='approved').count(),
                    'pending_certificates': user_certificates.filter(status='pending').count(),
                    'expiring_soon': user_certificates.filter(
                        expiry_date__isnull=False,
                        expiry_date__lte=today + timedelta(days=30),
                        expiry_date__gt=today
                    ).count(),
                }
                
                print(f"  Stats: {stats}")
                
            except Exception as e:
                print(f"  ❌ Error: {e}")
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    test_certificate_dashboard_data()
