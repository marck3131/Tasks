from GUI import GUI
from HAL import HAL
# Enter sequential code!
import cv2

HAL.takeoff(1)
ix , iy , iz = -3.20, -1.00, 1.50
HAL.set_cmd_pos(-3.20, -1.00, 2, 0)

greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

while True:
    # Enter iterative code!
    cap_front = HAL.get_frontal_image()
    cap = HAL.get_ventral_image()

    # Convert the frame to the HSV color space
    hsv = cv2.cvtColor(cap, cv2.COLOR_BGR2HSV)

    # Construct a mask for the green color of the TurtleBot
    mask = cv2.inRange(hsv, greenLower, greenUpper)

    # Apply a series of morphological operations to the mask to remove any small blobs left in the mask
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if any contours were found
    if len(contours) > 0:
        # Find the largest contour
        c = max(contours, key=cv2.contourArea)

        # Find the centroid of the largest contour
        M = cv2.moments(c)
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        # Draw a circle at the centroid of the largest contour
        cv2.circle(cap, (cx, cy), 5, (0, 0, 255), -1)

        # Convert the centroid to a position in meters relative to the drone
        height, width, _ = cap.shape
        x = (cx - width / 2) / width * 2.0
        y = (cy - height / 2) / height * 2.0

        # Send a command to the drone to follow the TurtleBot (replace with your own code)
        print(f"Moving drone to follow TurtleBot: x={x}, y={y}")
        HAL.set_cmd_pos(ix+x, iy+y, iz, 0)

    # Show the frame in the GUI
    GUI.showImage(cap)
    GUI.showLeftImage(cap_front)

    # Wait for a small amount of time to prevent the drone from sending too many commands too quickly
    cv2.waitKey(100)
