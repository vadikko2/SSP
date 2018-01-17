import cv2, os,sys
import numpy as np
from PIL import Image

face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')

def get_images_and_labels(path):
   
    dir_list = os.listdir(path)

    images = []
   
    labels = []
    count = 1
    
    for dir1 in dir_list:  
        
        if dir1 !='.directory':
            images_paths = os.listdir(path + '/' + dir1)
            for image_path in images_paths:
                if '.png' in image_path:
                    image_pil = Image.open(path + '/' + dir1 + '/' + image_path).convert('L')
                    image = np.array(image_pil, 'uint8')
                
                    faces = face_cascade.detectMultiScale(image)
                    for (x, y, w, h) in faces:
                        face = cv2.resize(image[y: y + h, x: x + w],(150,150))
                        images.append(face)
                        labels.append(count)
                        cv2.imshow(dir1 + str(count),face)
                        cv2.waitKey(50)
                
            count = count + 1
            
    return images, labels


path = "./db"

images, labels = get_images_and_labels(path)
cv2.destroyAllWindows()

if sys.argv[1] == 'Eigen':
    recognizer = cv2.face.createEigenFaceRecognizer()
elif sys.argv[1] == 'Fisher':
     recognizer = cv2.face.createFisherFaceRecognizer()
elif sys.argv[1] == 'LBPH':
     recognizer = cv2.face.createLBPHFaceRecognizer()
     


recognizer.train(images, np.array(labels))
recognizer.save("model_" + sys.argv[1])
