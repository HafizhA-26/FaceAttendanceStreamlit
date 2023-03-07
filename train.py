import cv2
import face_recognition
import os

path = 'images/sample_images'
images = []
classNamesTrain = []
classIDTrain = []
myList = os.listdir(path)
img_counter = 0
for cl in myList:
    for cl2 in os.listdir(path+"/"+cl):
        currentImage = cv2.imread(f'{path}/{cl}/{cl2}')
        images.append(currentImage)
        filename = os.path.splitext(cl)[0]
        id = filename.split('_')[0]
        nama = filename.split('_')[1]
        classIDTrain.append(id)
        classNamesTrain.append(nama)

def findEncoding(images):
    encodeList = []
    persentfile = (1 / len(images)) * 100
    curprogress = 0
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
        curprogress += persentfile
        print("collecting data sample : "+ str(int(curprogress)) + "%")

    return encodeList
