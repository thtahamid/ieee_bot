import cv2
import numpy as np

def detect_color():
    # Define the lower and upper boundaries for red and blue colors in the HSV color space
    red_lower = np.array([0, 120, 70])
    red_upper = np.array([10, 255, 255])
    blue_lower = np.array([94, 80, 2])
    blue_upper = np.array([126, 255, 255])

    # Initialize the camera
    cap = cv2.VideoCapture(0)

    try:
        while True:
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
            elif blue_percentage > red_percentage:
                color = "Blue"
            else:
                color = "None"
            
            print(f"Detected color: {color}")
            # return color

            # Add a small delay to avoid flooding the terminal
            cv2.waitKey(1000)

    except KeyboardInterrupt:
        print("Program interrupted by user")

    finally:
        # Release the capture and close any OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

# Example usage of the function
if __name__ == "__main__":
    detect_color()
    # while True:
    #     color = detect_color()
    #     print(color)
