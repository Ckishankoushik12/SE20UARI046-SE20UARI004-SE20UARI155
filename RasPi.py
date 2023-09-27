import RPi.GPIO as GPIO
import time
import pyrebase

# Firebase configuration (update with your Firebase credentials)
firebase_config = {
    'apiKey': "YOUR_API_KEY",
    'authDomain': "YOUR_AUTH_DOMAIN",
    'projectId': "YOUR_PROJECT_ID",
    'storageBucket': "YOUR_STORAGE_BUCKET",
    'messagingSenderId': "YOUR_MESSAGING_SENDER_ID",
    'appId': "YOUR_APP_ID",
    'databaseURL': 'YOUR_DATABASE_URL',
    'measurementId': "YOUR_MEASUREMENT_ID"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

# Ultrasonic sensor pins
TRIG_PIN = 18
ECHO_PIN = 24

def setup_gpio():
    """Setup GPIO pins for the ultrasonic sensor."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)

def cleanup_gpio():
    """Clean up and reset GPIO configuration."""
    GPIO.cleanup()

def measure_distance():
    """Measure distance using the ultrasonic sensor."""
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        stop_time = time.time()

    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  # Speed of sound is 343 m/s
    return distance

def push_data_to_firebase(distance):
    """Push distance data to Firebase."""
    data = {
        "distance": distance,
        "timestamp": int(time.time())
    }
    db.child("Status").push(data)

if __name__ == "__main__":
    try:
        setup_gpio()
        
        while True:
            distance = measure_distance()
            print(f"Distance: {distance} cm")
            
            push_data_to_firebase(distance)

            time.sleep(1)  # Wait for 1 second before the next reading

    except KeyboardInterrupt:
        cleanup_gpio()
