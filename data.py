import cv2, sys
from datetime import datetime

face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')
    
name = sys.argv[1]
cap = cv2.VideoCapture(0)


counter = 0 

while True or counter < 10:
    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detected_faces = face_cascade.detectMultiScale(gray)
    for (x, y, w, h) in detected_faces:
        face = img[y:y + h, x: x + w]
        cv2.imwrite('./db/' + name + '/' + str(datetime.now()) + '.png', face)
        cv2.imshow('face', face)
        counter = counter + 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break    
    
cap.release()
cv2.distroyAllWindows()
