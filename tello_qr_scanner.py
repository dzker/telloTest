import cv2
import numpy as np
from pyzbar.pyzbar import decode
from djitellopy import Tello

# Initialize the Tello drone
tello = Tello()

# Connect to the Tello drone
tello.connect()

# Start the video stream
tello.streamon()

# Get the video feed
frame_read = tello.get_frame_read()

# Function to scan for QR codes in the frame
def scan_qr_codes(frame):
    # Convert the frame to grayscale (for better QR code detection)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Decode the QR codes in the frame
    qr_codes = decode(gray)

    # Loop over detected QR codes
    for qr_code in qr_codes:
        # Get the data from the QR code
        qr_data = qr_code.data.decode('utf-8')
        print(f"QR Code detected: {qr_data}")

        # Draw a rectangle around the QR code
        points = qr_code.polygon
        if len(points) == 4:
            pts = [(point.x, point.y) for point in points]
            pts = np.array(pts, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=3)

        # Put the QR code data as text on the frame
        cv2.putText(frame, qr_data, (qr_code.rect.left, qr_code.rect.top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return frame

# Display video feed and scan for QR codes
while True:
    # Get the current frame from the Tello
    frame = frame_read.frame

    # Scan for QR codes in the frame
    frame = scan_qr_codes(frame)

    # Display the video feed with QR code detection
    cv2.imshow("Tello Camera with QR Code Scanning", frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop the video stream and clean up
cv2.destroyAllWindows()
tello.streamoff()
