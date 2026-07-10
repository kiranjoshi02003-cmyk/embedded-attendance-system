#include <Adafruit_Fingerprint.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Hardware Serial2 for R503
HardwareSerial mySerial(2);
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  Serial.begin(115200);
  lcd.init();
  lcd.backlight();
  
  finger.begin(57600);
  
  if (finger.verifyPassword()) {
    lcd.print("Sensor Ready");
  } else {
    lcd.print("Sensor Error");
    while (1);
  }
  delay(2000);
  lcd.clear();
}

void loop() {
  lcd.setCursor(0, 0);
  lcd.print("Place Finger...");

  int p = finger.getImage();
  if (p != FINGERPRINT_OK) return;

  p = finger.image2Tz();
  if (p != FINGERPRINT_OK) return;

  p = finger.fingerFastSearch();
  if (p == FINGERPRINT_OK) {
    lcd.clear();
    lcd.print("ID Found: #");
    lcd.print(finger.fingerID);
    
    // TODO: Send finger.fingerID to your Flask server here!
    
    delay(3000);
    lcd.clear();
  } else {
    lcd.clear();
    lcd.print("Unknown Print");
    delay(2000);
    lcd.clear();
  }
}