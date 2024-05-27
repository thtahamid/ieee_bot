import cv2
import numpy as np
from flask import Flask, render_template, Response

app = Flask(__name__)

# Initialize the camera
cap = cv2.VideoCapture(0)

# Define the lower and upper boundaries for red and blue colors in the HSV color space
red_lower = np.array([0, 120, 70])
red_upper = np.array([10, 255, 255])
blue_lower = np.array([94, 80, 2])
blue_upper = np.array([126, 255, 255])

def generate_frames():
    while True:
        try:
            # Capture frame-by-frame
            ret, frame = cap.read()
            
            if not ret:
                print("Failed to grab frame")
                break

            # Convert the frame to the HSV color space
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Create masks for red and blue colors
            red_mask = cv2.inRange(hsv, red_lower, red_upper)
            blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
            
            # Calculate the percentage of each color in the frame
            red_percentage = (cv2.countNonZero(red_mask) / (frame.size / 3)) * 100
            blue_percentage = (cv2.countNonZero(blue_mask) / (frame.size / 3)) * 100
            
            # Determine which color is dominant
            if red_percentage > blue_percentage:
                color = "Red"
                cv2.putText(frame, "Detected Color: Red", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            elif blue_percentage > red_percentage:
                color = "Blue"
                cv2.putText(frame, "Detected Color: Blue", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            else:
                color = "None"
                cv2.putText(frame, "Detected Color: None", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame in byte format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        except Exception as e:
            print(f"Error: {e}")
            break

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"Failed to start Flask app: {e}")
