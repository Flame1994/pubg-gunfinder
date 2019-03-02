import numpy as np
import cv2
from PIL import ImageGrab as ig
import time
import pyautogui
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
print(pyautogui.size().width)
last_time = time.time()
screen_width = pyautogui.size().width
screen_height = pyautogui.size().height
print(screen_width - 100)

while(True):
    screen = ig.grab(bbox=(1200,70,1920,300))
    #print('Loop took {} seconds',format(time.time()-last_time))
    gray = cv2.cvtColor(np.array(screen), cv2.COLOR_BGR2GRAY)    
    blurred = cv2.blur(gray, (3,3))
    cv2.imshow("test", blurred)
    output = pytesseract.image_to_string(blurred, lang='eng')
    if len(output):
        print(output)
    last_time = time.time()
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break