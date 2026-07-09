from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    students = db.relationship('Student', backref='department', lazy=True)

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    # Store binary biometric data instead of an Integer ID
    fingerprint_template = db.Column(db.LargeBinary, nullable=False) 
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    attendances = db.relationship('Attendance', backref='student', lazy=True)

class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    mac_address = db.Column(db.String(17), unique=True, nullable=False)
    location = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), default='offline') # Tracks if ESP32 is online

class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    scan_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    scan_time = db.Column(db.Time, nullable=False, default=datetime.utcnow().time)
    
    # ADD THIS LINE BELOW
    device = db.relationship('Device', backref='attendances')