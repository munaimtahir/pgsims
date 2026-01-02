import sqlite3
import os

# Path to the SQLite database
db_path = 'd:/PMC/sims_project-2/db.sqlite3'

if os.path.exists(db_path):
    print("=== SIMS DATABASE USER ANALYSIS ===\n")
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if users_user table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users_user';")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("✅ users_user table found!")
            
            # Get user count
            cursor.execute("SELECT COUNT(*) FROM users_user;")
            user_count = cursor.fetchone()[0]
            print(f"📊 Total Users: {user_count}")
            
            if user_count > 0:
                print("\n👥 USER DETAILS:")
                print("-" * 80)
                
                # Get all user information
                cursor.execute("""
                    SELECT 
                        id, username, first_name, last_name, email, role, 
                        specialty, year, is_active, is_staff, is_superuser,
                        date_joined, last_login
                    FROM users_user 
                    ORDER BY date_joined DESC
                """)
                
                users = cursor.fetchall()
                
                for user in users:
                    user_id, username, first_name, last_name, email, role, specialty, year, is_active, is_staff, is_superuser, date_joined, last_login = user
                    
                    full_name = f"{first_name} {last_name}".strip() or "Not provided"
                    
                    print(f"ID: {user_id}")
                    print(f"Username: {username}")
                    print(f"Full Name: {full_name}")
                    print(f"Email: {email or 'Not provided'}")
                    print(f"Role: {role}")
                    print(f"Specialty: {specialty or 'Not specified'}")
                    print(f"Year: {year or 'Not specified'}")
                    print(f"Active: {'Yes' if is_active else 'No'}")
                    print(f"Staff: {'Yes' if is_staff else 'No'}")
                    print(f"Superuser: {'Yes' if is_superuser else 'No'}")
                    print(f"Date Joined: {date_joined}")
                    print(f"Last Login: {last_login or 'Never'}")
                    print("-" * 80)
                
                # Role summary
                print("\n📈 ROLE SUMMARY:")
                cursor.execute("SELECT role, COUNT(*) FROM users_user GROUP BY role;")
                role_counts = cursor.fetchall()
                for role, count in role_counts:
                    print(f"  {role}: {count} users")
                
                # Active vs Inactive
                print("\n🔄 STATUS SUMMARY:")
                cursor.execute("SELECT is_active, COUNT(*) FROM users_user GROUP BY is_active;")
                status_counts = cursor.fetchall()
                for is_active, count in status_counts:
                    status = "Active" if is_active else "Inactive"
                    print(f"  {status}: {count} users")
                    
            else:
                print("\n❌ No users found in the database.")
                print("\n💡 To create users:")
                print("   1. Create superuser: py manage.py createsuperuser")
                print("   2. Use Django admin: http://127.0.0.1:8000/admin/")
                print("   3. Use user management: http://127.0.0.1:8000/users/create/")
        else:
            print("❌ users_user table not found!")
            print("Run migrations: py manage.py migrate")
            
        conn.close()
        
    except Exception as e:
        print(f"❌ Error accessing database: {e}")
        
else:
    print("❌ Database file not found at:", db_path)
    print("Run migrations first: py manage.py migrate")
