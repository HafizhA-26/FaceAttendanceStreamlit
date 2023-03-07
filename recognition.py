import cv2
import time as t
import os
import numpy as np
import face_recognition
import train
import streamlit as st
from datetime import datetime,time

# Take data from train.py to classify the faces
classNames = train.classNamesTrain                              # Take name list
classID = train.classIDTrain                                    # Take ID List
unknownface = []

# Other Variables
storagepath = 'storage/'                                        # storage path to store data
nowdir = storagepath+datetime.now().strftime('%d-%m-%Y')        # variable to store today directory
name = ""                                                       # variable to show the name of classified face

saveAttendance = False

# office's enter hours
enterHours = time(8,0,0).strftime('%H:%M:%S')
if "jamMasuk" in st.session_state:
    enterHours = time(st.session_state['jamMasuk'],0,0).strftime('%H:%M:%S')

# Function to encode faces
def trainData():
    return train.findEncoding(train.images)

# function for checking today directory, is it exists or no
# if it's no it will make the directory
def checkDir():
    if not os.path.exists(nowdir):
        os.mkdir(nowdir)                                        # make today directory
        os.mkdir(nowdir+"/"+"attendance_photo")                 # make today directory for saving attendance photos
        os.mkdir(nowdir+"/"+"unknown")                          # make today directory for saving unknown faces
        os.mkdir(nowdir + "/" + "custom")                       # make today directory for saving custom faces
        cs = open(nowdir+"/"+"attendance_data.csv","w+")        # make today csv file for marking the attendance
        cs.writelines("ID,Name,Time,Status")                    # make first line of the csv file
        cs.close()
checkDir()

# function to insert a row when it's detecting face
def markAttendace(name ,id):
    with open(nowdir+'/attendance_data.csv','r+') as f:         # open today csv file
        idList = []                                             # temporary variable to store entered id
        for line in f:                                          # take line by line from the csv file
            entry = line.split(',')                             # split the line from ,
            idList.append(entry[0])                             # enter the id from file to idList
        if id not in idList:                                    # check if there is no id from people whose faces have been detected
            now = datetime.now()
            stat = ""                                           # variable status is it late or on time
            datestring = now.strftime('%H:%M:%S')
            if datestring > enterHours:
                stat = "Late"
            elif datestring <= enterHours:
                stat = "On Time"
            f.writelines(f'\n{id},{name},{datestring},{stat}')  # write a row to csv the file
            return "once"                                       # return 'once' to trigger attendance photo
        else:
            return ""

def captureAttendance(cap, frameShow, encodeListKnown):
    success, img = cap.read()
    isTakePhoto = ""
    imgS = cv2.resize(img,(0,0),None, 0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS,faceCurFrame)
    if len(encodeListKnown) > 0:
        if not faceCurFrame:
            cv2.putText(img, "No face detected", (30 , 460), cv2.FONT_HERSHEY_COMPLEX, .8, (100, 100, 255), 2);
        for encodeFace, faceLoc in zip(encodeCurFrame,faceCurFrame):
            mathces = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)
            if mathces[matchIndex] and np.amin(faceDis) < 0.5:
                name = classNames[matchIndex].upper()
                shortName = ""
                if len(name.split(" ")) > 1:
                    shortName = name.split(" ")[0] + " " +name.split(" ")[1]
                else:
                    shortName = name.split(" ")[0]
                id = classID[matchIndex]
                y1,x2,y2,x1 = faceLoc
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1-10,y1-3),(x2+10,y2+3),(0,255,0) ,2)
                cv2.rectangle(img,(x1-10,y2+30),(x2+10,y2),(0,255,0) ,cv2.FILLED)
                cv2.putText(img, (id +" - "+shortName), (x1 + 3, y2 + 20), cv2.FONT_HERSHEY_COMPLEX, .4, (255, 255, 255), 2)
                isTakePhoto = markAttendace(name,id)
            else :
                name = "unknown"
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1 - 5, y1), (x2 + 5, y2), (0, 0, 255), 2)
                cv2.rectangle(img, (x1 - 5, y2 + 25), (x2 + 5, y2), (0, 0, 255), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 + 15), cv2.FONT_HERSHEY_COMPLEX, .4, (255, 255, 255), 2)
                isTakePhoto = "unknown"                                                                                 # change isTakePhoto to 'unknown' to trigger the unknown face photo
    frameShow.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    if isTakePhoto == "once":
        # take attendance photo to attendance photo directory
        cv2.imwrite(nowdir+'/attendance_photo/'+name+'.jpg', img)
        # reset isTakePhoto variable
        isTakePhoto = ""

    elif isTakePhoto == "unknown" and t.time() > st.session_state['unknownPauseTime']:
        imgUnknown = cv2.resize(img,(0,0),None, 0.5,0.5)
        # take unknown face photo to unknown face photo directory
        cv2.imwrite(nowdir+'/unknown/unknown_'+datetime.now().strftime('%H-%M-%S')+'.jpg', imgUnknown)
        # reset isTakePhoto variable
        isTakePhoto = ""
        st.session_state['unknownPauseTime'] = t.time() + st.session_state['unknownPause']

    if st.session_state['customTake']:
        photopath = nowdir+'/custom/'
        # save custom photo to custom photo directory
        cv2.imwrite(photopath+"saved_photo_"+datetime.now().strftime('%H-%M-%S')+".jpg ", img)
        st.session_state['customTake'] = False