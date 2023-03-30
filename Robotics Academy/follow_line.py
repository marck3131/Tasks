from GUI import GUI
from HAL import HAL
import cv2
import numpy as np
import time

#define speed of the f1
const_speed = 3

#define constants for PID
kp = 0.0285
ki = 0.000001
kd = 0.055
prev_error = 0
cummulative_area = 0

def Masking(capt, result):
  
    lower1 = np.array([0, 100, 20])
    lower2 = np.array([160,100,20])
    upper1 = np.array([10, 255, 255])
    upper2 = np.array([179,255,255])
    
    lower_mask = cv2.inRange(capt, lower1, upper1)
    upper_mask = cv2.inRange(capt, lower2, upper2)
    
    avg_mask = lower_mask + upper_mask
  
    masked = cv2.bitwise_and(result, result, mask=avg_mask)

    return (masked, avg_mask)
    
def PID(error):
    global prev_error, cummulative_area

    delta_error = error - prev_error
    cummulative_area += error
  
    p_term = kp * error 
    i_term = ki * cummulative_area
    d_term = kd * delta_error
    
    deviation = p_term + d_term + i_term

    prev_error = error

    #setting limits
    if deviation > 75:
        deviation = 75
    elif deviation < -75:
        deviation = -75
        
    return deviation 

while True:
    capt = HAL.getImage()
    result = capt.copy()
    hsv = cv2.cvtColor(capt, cv2.COLOR_BGR2HSV)
    (masked, mask) = Masking(hsv, result)
    M = cv2.moments(mask)
 
    if M['m00'] > 0:
        c_x = int(M["m10"]/M["m00"])
        c_y = int(M["m01"]/M["m00"])
        cv2.circle(capt, (c_x, c_y), 5, (0, 200, 0), -1)
        
        GUI.showImage(capt)
        
        error = masked.shape[1]/2 - c_x  
        
        
        #PID Function, returns the angle required
        deviation = PID(error) / 10

        HAL.setV(const_speed)
        if (not (error < 5 and error > -5)):
            HAL.setW(deviation)
       
    time.sleep(3 / 1000) 
