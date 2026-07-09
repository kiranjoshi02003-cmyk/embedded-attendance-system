import sqlite3
import base64

# Connect to the database
conn = sqlite3.connect('instance/smart_attendance.db')
cursor = conn.cursor()

# The sample template provided
sample_template = "SGVsbG8gYmlvc3luYyBwcm8hIFRoaXMgaXMgYSBzYW1wbGUgYmlvbWV0cmljIHRlbXBsYXRlIGJsb2IgZ2VuZXJhdGVkIGZvciB0ZXN0aW5nIHB1cnBvc2VzIGFuZCBzZWN1cml0eSB2YWxpZGF0aW9uIGluIHlvdXIgc3lzdGVtLiBUaGlzIHN0cmluZyBjYW4gYmUgZGVjb2RlZCBpbnRvIGJpbmFyeSBkYXRhIGZvciBTZXJ2ZXItU2lkZSBNYXRjaGluZy4="
binary_template = base64.b64decode(sample_template)

# Insert the student with the binary template
# Note: Ensure department_id 1 exists (run a separate script or insert it first)
query = "INSERT INTO students (roll_number, full_name, fingerprint_template, department_id) VALUES (?, ?, ?, ?)"
data = ('CS101', 'John Doe', binary_template, 1)

try:
    cursor.execute(query, data)
    conn.commit()
    print("Student added with template successfully!")
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()