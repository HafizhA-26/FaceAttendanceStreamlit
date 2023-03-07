# File : attendance_data.py
# Created By : Muhammad Hafizh Auliansyah
# Last Modified : 7 March 2023

import streamlit as st
import numpy as np
import cv2
from PIL import Image
import os
import shutil

formCompleted = True

# Function to check is id already exists or not
def checkIdNotDuplicate(id):
    saved_path = os.path.join("images", "sample_images")
    for folder_name in os.listdir(saved_path):
        if folder_name.split('_')[0] == str(id):
            return False
    return True

# Function to delete saved person data, including folder and images
def deleteSavedData(id):
    saved_path = os.path.join("images", "sample_images")
    for folder_name in os.listdir(saved_path):
        if folder_name.split('_')[0] == str(id):
            print("")
            delete_path = os.path.join(saved_path, folder_name)
            if os.path.isdir(delete_path):
                shutil.rmtree(delete_path)

# Function to convert uploaded data into OpenCV Format
def convertToCV(foto_upload):
    foto_upload_np = np.asarray(bytearray(foto_upload.read()), dtype=np.uint8)
    foto_upload_np = cv2.imdecode(foto_upload_np, 1)
    return foto_upload_np


st.title("Attendance Data")

# Section : Saved Data
st.markdown("***")
st.markdown("## Saved Data")
st.text("Data yang tersimpan")
listPeople = os.listdir('images/sample_images')
for p in listPeople:
    col1, col2 = st.columns([1, 3])
    with col1:
        photos = os.listdir('images/sample_images/'+p)
        if len(photos) > 0:
            photo = Image.open('images/sample_images/'+p+'/'+photos[0])
            st.image(photo)
    with col2:
        dataP = p.split('_')
        id = dataP[0]
        name = dataP[1]
        st.markdown("ID : "+id)
        st.markdown("Nama Lengkap : "+name)
        if st.button(label="Delete Data", key=id):
            deleteSavedData(id)
            st.experimental_rerun()

# Section Upload New Person data
st.markdown("***")
st.markdown("## Upload New Data")
st.text("Upload data orang baru untuk absensi")
with st.form("newPeople"):
    # Form input new data
    id = st.text_input('ID', placeholder="Masukkan ID")
    name = st.text_input('Nama Lengkap', placeholder="Masukkan nama")
    foto_upload1 = st.file_uploader("Foto 1 (Wajib)",
        ['png', 'jpg', 'jpeg'],
        help="Foto untuk rekognisi 1"
        )
    foto_upload2 = st.file_uploader("Foto 2 (Wajib)",
        ['png', 'jpg', 'jpeg'],
        help="Foto untuk rekognisi 2",
        )
    foto_upload3 = st.file_uploader("Foto 3 (Wajib)",
        ['png', 'jpg', 'jpeg'],
        help="Foto untuk rekognisi 3"
        )
    foto_upload4 = st.file_uploader("Foto 4 (Opsional)",
        ['png', 'jpg', 'jpeg'],
        help="Foto untuk rekognisi 4"
        )
    foto_upload5 = st.file_uploader("Foto 5 (Opsional)",
        ['png', 'jpg', 'jpeg'],
        help="Foto untuk rekognisi 5"
        )

    submitted = st.form_submit_button("Save")
    if submitted:
        if id is None or name is None or foto_upload1 is None or foto_upload2 is None or foto_upload3 is None:
            st.markdown(":red[Form belum lengkap !!!]")
        elif checkIdNotDuplicate(id) is False:
            st.markdown(":red[ID Sudah Ada!!!]")
        else:
            folderName = id + "_" + name
            dirName = 'images/sample_images/'+folderName
            if os.path.exists(dirName) is False:
                os.mkdir(dirName)
            fileName1 = foto_upload1.name.split('.')
            foto_upload1.name = "1."+fileName1[1]
            fileName2 = foto_upload2.name.split('.')
            foto_upload2.name = "2." + fileName2[1]
            fileName3 = foto_upload3.name.split('.')
            foto_upload3.name = "3." + fileName3[1]
            f1_cv = convertToCV(foto_upload1)
            cv2.imwrite(dirName + "/" + foto_upload1.name, f1_cv)
            f2_cv = convertToCV(foto_upload2)
            cv2.imwrite(dirName + "/" + foto_upload2.name, f2_cv)
            f3_cv = convertToCV(foto_upload3)
            cv2.imwrite(dirName + "/" + foto_upload3.name, f3_cv)
            if foto_upload4 is not None:
                fileName4 = foto_upload4.name.split('.')
                foto_upload4.name = "3." + fileName4[1]
                f4_cv = convertToCV(foto_upload4)
                cv2.imwrite(dirName + "/" + foto_upload4.name, f4_cv)
            if foto_upload5 is not None:
                fileName5 = foto_upload5.name.split('.')
                foto_upload5.name = "3." + fileName5[1]
                f5_cv = convertToCV(foto_upload5)
                cv2.imwrite(dirName + "/" + foto_upload5.name, f5_cv)
            st.success("Berhasil Menyimpan Data Baru")
            st.experimental_rerun()
