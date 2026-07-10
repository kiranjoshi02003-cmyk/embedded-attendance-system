import os
from app import app, db

def reset_database():
    db_path = 'instance/smart_attendance.db'
    
    # 1. Delete the old database file if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Existing database deleted.")
    else:
        print("No database file found.")

    # 2. Recreate the database structure
    with app.app_context():
        db.create_all()
        print("Database schema reset successfully with new Template-based structure.")

if __name__ == "__main__":
    reset_database()