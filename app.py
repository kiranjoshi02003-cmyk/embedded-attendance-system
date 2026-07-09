import base64
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from datetime import datetime
from scipy.spatial import distance
from config import Config
from models import db, Student, Device, Attendance, Department

# ==========================================
# 1. APP INITIALIZATION
# ==========================================
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(Config)

db.init_app(app)
CORS(app)
jwt = JWTManager(app)

# ==========================================
# 2. FRONTEND UI ROUTES
# ==========================================
@app.route('/')
def home():
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/students', methods=['GET'])
def students_page():
    return render_template('students.html', students=Student.query.all(), departments=Department.query.all())

@app.route('/attendance', methods=['GET'])
def attendance_page():
    return render_template('attendance.html', records=Attendance.query.order_by(Attendance.scan_date.desc(), Attendance.scan_time.desc()).all())

@app.route('/devices', methods=['GET'])
def devices_page():
    return render_template('devices.html', devices=Device.query.all())

# ==========================================
# 3. BACKEND API ROUTES
# ==========================================

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    if data.get('username') == 'admin' and data.get('password') == 'admin123':
        return jsonify(access_token=create_access_token(identity='admin')), 200
    return jsonify({"msg": "Bad credentials"}), 401

@app.route('/api/attendance', methods=['POST'])
def mark_attendance():
    data = request.get_json()
    mac_address = data.get('mac_address')
    timestamp_str = data.get('timestamp')
    
    # 1. Decode incoming binary template
    try:
        received_template = list(base64.b64decode(data.get('template_data')))
    except Exception:
        return jsonify({"status": "error", "message": "Invalid template format"}), 400
    
    # 2. Authenticate Device
    device = Device.query.filter_by(mac_address=mac_address).first()
    if not device:
        return jsonify({"status": "error", "message": "Unauthorized device"}), 401

    # 3. Biometric Matching (Server-side)
    all_students = Student.query.all()
    matched_student = None
    THRESHOLD = 0.5 # Sensitivity threshold
    
    for student in all_students:
        stored_template = list(student.fingerprint_template)
        if distance.euclidean(received_template, stored_template) < THRESHOLD:
            matched_student = student
            break

    if not matched_student:
        return jsonify({"status": "error", "message": "No match found"}), 404

    # 4. Record Attendance
    scan_dt = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
    if not Attendance.query.filter_by(student_id=matched_student.id, scan_date=scan_dt.date()).first():
        db.session.add(Attendance(student_id=matched_student.id, device_id=device.id, scan_date=scan_dt.date(), scan_time=scan_dt.time()))
        db.session.commit()

    return jsonify({"status": "success", "message": "Verified", "name": matched_student.full_name}), 201

# [Existing Dashboard and Feed endpoints...]
@app.route('/api/dashboard/stats', methods=['GET'])
@jwt_required() 
def get_stats():
    total = Student.query.count()
    present = Attendance.query.filter_by(scan_date=datetime.utcnow().date()).count()
    return jsonify({"total_students": total, "present_today": present, "absent_today": total - present}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(host='0.0.0.0', port=5000, debug=True)