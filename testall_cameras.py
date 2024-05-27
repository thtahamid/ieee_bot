import cv2

def test_camera(device_index):
    cap = cv2.VideoCapture(device_index)
    if not cap.isOpened():
        print(f"Error: Could not open video capture for device {device_index}")
        return False
    else:
        print(f"Camera {device_index} opened successfully")
        cap.release()
        return True

def main():
    video_devices = [
        "/dev/video0", "/dev/video1", "/dev/video2", "/dev/video10",
        "/dev/video11", "/dev/video12", "/dev/video13", "/dev/video14",
        "/dev/video15", "/dev/video16", "/dev/video18", "/dev/video19",
        "/dev/video20", "/dev/video21", "/dev/video22", "/dev/video23",
        "/dev/video31"
    ]

    for device in video_devices:
        device_index = int(device.replace('/dev/video', ''))
        if test_camera(device_index):
            break

if __name__ == "__main__":
    main()
