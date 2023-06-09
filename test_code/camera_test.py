import cv2
import numpy as np

cap = cv2.VideoCapture(0)
while True:
    ret,frame = cap.read()
    img = cv2.resize(frame, (200,200))
    # img_ = cv2.resize(frame, (640,480))
    cv2.imshow("wwww",img)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()