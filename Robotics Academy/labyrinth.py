from GUI import GUI
from HAL import HAL
# Enter sequential code!

import cv2
import numpy as np

HAL.takeoff(1)

lower_green = np.array([36, 25, 25])
upper_green = np.array([70, 255, 255])

while True:
    # Enter iterative code!
        # Threshold the image to get only the green pixels
    cap=HAL.get_ventral_image()
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(cap, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Find the contours of the green regions
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Get the bounding rectangles of the green regions
    rectangles = [cv2.boundingRect(c) for c in contours]
    
    # Loop over each bounding rectangle
    for rect in rectangles:
        # Get the x, y, width, and height of the rectangle
        x, y, w, h = rect
    
        # Calculate the aspect ratio of the bounding rectangle
        aspect_ratio = w / float(h)
    
        # Check if the aspect ratio is within a certain range
        if aspect_ratio >= 0.5 and aspect_ratio <= 2.0:
            # Split the rectangle in half horizontally and vertically
            half_height = h // 2
            half_width = w // 2
    
            # Get the number of green pixels in each quadrant
            top_pixels = np.sum(mask[y:y+half_height, x:x+w])
            bottom_pixels = np.sum(mask[y+half_height:y+h, x:x+w])
            left_pixels = np.sum(mask[y:y+h, x:x+half_width])
            right_pixels = np.sum(mask[y:y+h, x+half_width:x+w])
    
            # Determine the direction based on the number of green pixels in each quadrant
            if top_pixels > (w * half_height) // 2 and bottom_pixels < (w * half_height) // 4:
                print('reverse')
            elif left_pixels > right_pixels and top_pixels < bottom_pixels:
                print('left')
                HAL.set_cmd_vel(0, 0.25, 0, 0)
            elif right_pixels > left_pixels and top_pixels < bottom_pixels:
                print('right')
            else:
                print('straight')
                HAL.set_cmd_vel(0, 0.26, 0, 0)
                
GUI.showImage(cap)
