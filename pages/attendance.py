import streamlit as st
import cv2
from PIL import Image
import recognition
import numpy as np
import pandas as pd
import time as t
from datetime import datetime
import os

if "cameraOn" not in st.session_state:
    st.session_state['cameraOn'] = False
if "encodedData" not in st.session_state:
    st.session_state['encodedData'] = []
if "todayData" not in st.session_state:
    st.session_state['todayData'] = pd.read_csv(recognition.nowdir+"/attendance_data.csv")
if "unknownPause" not in st.session_state:
    st.session_state['unknownPause'] = 1
if "jamMasuk" not in st.session_state:
    st.session_state['jamMasuk'] = 8

st.session_state['unknownPauseTime'] = t.time() + st.session_state['unknownPause']
st.session_state['customTake'] = False

todayData = st.session_state['todayData']
encodeListKnown = st.session_state['encodedData']
run = False


st.set_page_config(
        page_title="Attendace Check"
    )
def color_status(s):
    return np.where(s.eq("Late"), 'background-color: red', 'background-color: green')


st.title("Cek Kehadiran")
st.markdown("***")

if st.button("Train Data"):
    if len(encodeListKnown) == 0:
        encodeListKnown = recognition.trainData()
        st.session_state['encodedData'] = encodeListKnown

my_bar = st.progress(len(encodeListKnown), text="Trained Data")
my_bar.progress(len(encodeListKnown)/len(encodeListKnown) if len(encodeListKnown) > 0 else 0, text="Trained Data")

col1,col2, col3 = st.columns(3)
with col1:
    if st.button("Run Check"):
        st.session_state['cameraOn'] = True
with col2:
    if st.button("Take Photo"):
        st.session_state['customTake'] = True
with col3:
    if st.button("Stop Check"):
        st.session_state['cameraOn'] = False
        cap = None

img_file_buffer = st.image([])
cap = cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) if st.session_state['cameraOn'] else None
while st.session_state['cameraOn']:
    recognition.captureAttendance(cap, img_file_buffer, encodeListKnown)

# Kehadiran Hari Ini
st.markdown("***")
st.markdown("## Kehadiran hari ini")
st.markdown("Batas Jam Masuk : " + str(st.session_state['jamMasuk']) + ":00")
if st.button("Update Data"):
    st.session_state['todayData'] = pd.read_csv(recognition.nowdir+"/attendance_data.csv")
    todayData = st.session_state['todayData']
donwloadPD = pd.read_csv(recognition.nowdir+"/attendance_data.csv")
downloadCSV = donwloadPD.to_csv().encode('utf-8')
st.download_button(
    label="Download Data",
    data=downloadCSV,
    file_name='Kehadiran '+datetime.now().strftime('%d-%m-%Y')+'.csv',
    mime='text/csv',
)
df = todayData
st.table(df.style.apply(color_status, subset=['Status']))
st.markdown("## Foto Kehadiran")
listAttend = os.listdir(recognition.nowdir+'/attendance_photo/')
for i in range(0, len(listAttend), 3):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(Image.open(recognition.nowdir + '/attendance_photo/' + listAttend[i]))
        name = listAttend[i].split('.')
        st.caption(name[0].title())
    if len(listAttend) > (i + 1):
        with col2:
            st.image(Image.open(recognition.nowdir + '/attendance_photo/' + listAttend[i + 1]))
            name = listAttend[i+1].split('.')
            st.caption(name[0].title())
    if len(listAttend) > (i + 2):
        with col3:
            st.image(Image.open(recognition.nowdir + '/attendance_photo/' + listAttend[i + 2]))
            name = listAttend[i+2].split('.')
            st.caption(name[0].title())
# Section : Foto Diambil
st.markdown("***")
st.markdown("## Foto Diambil")
listCustom = os.listdir(recognition.nowdir+'/custom/')
for i in range(0, len(listCustom), 3):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(Image.open(recognition.nowdir+'/custom/'+listCustom[i]))
    if len(listCustom) > (i+1):
        with col2:
            st.image(Image.open(recognition.nowdir+'/custom/'+listCustom[i + 1]))
    if len(listCustom) > (i + 2):
        with col3:
            st.image(Image.open(recognition.nowdir + '/custom/' + listCustom[i + 2]))
# Wajah tidak dikenal
st.markdown("***")
st.markdown("## Wajah tidak dikenal")
listUnknown = os.listdir(recognition.nowdir+'/unknown/')
if st.button("Clear Today Unknown"):
    todayFolder = os.path.join(recognition.nowdir, "unknown")
    for filename in os.listdir(todayFolder):
        filePath = os.path.join(todayFolder, filename)
        try:
            if os.path.isfile(filePath) or os.path.islink(filePath):
                os.unlink(filePath)
        except Exception as e:
            print('Gagal delete %s. Karena: %s' % (filePath, e))
    st.experimental_rerun()
for i in range(0, len(listUnknown), 3):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(Image.open(recognition.nowdir+'/unknown/'+listUnknown[i]))
    if len(listUnknown) > (i+1):
        with col2:
            st.image(Image.open(recognition.nowdir+'/unknown/'+listUnknown[i + 1]))
    if len(listUnknown) > (i + 2):
        with col3:
            st.image(Image.open(recognition.nowdir + '/unknown/' + listUnknown[i + 2]))

