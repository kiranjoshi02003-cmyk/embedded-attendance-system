from app import app, db
from models import Device

def add_new_device(mac, location):
    with app.app_context():
        # Check if device already exists to avoid duplicates
        existing = Device.query.filter_by(mac_address=mac).first()
        if existing:
            print(f"Device with MAC {mac} already exists!")
            return

        # Create new device instance
        new_dev = Device(mac_address=mac, location=location, status='online')
        
        # Add to database
        db.session.add(new_dev)
        db.session.commit()
        print(f"Successfully added device: {mac} at {location}")

if __name__ == "__main__":
    # Add your device here
    add_new_device('AA:BB:CC:DD:EE:FF', 'Main Gate')