import streamlit as st
import pandas as pd
import os
from PIL import Image
from pages.attendance import color_status

storage_path = os.path.join("storage")
list_history = os.listdir(storage_path)

st.title("Attendance History")

# Section : History
st.markdown("***")
history_option = tuple(list_history)
history_choose = st.selectbox(
    "Pilih data absensi yang ingin ditampilkan : ", history_option
    )

history_path = os.path.join(storage_path, history_choose)
st.markdown("### Kehadiran Tanggal : "+ history_choose)
history_data = pd.read_csv(history_path+"/attendance_data.csv")
downloadCSV = history_data.to_csv().encode('utf-8')
st.download_button(
    label="Download Data",
    data=downloadCSV,
    file_name='Kehadiran '+history_choose+'.csv',
    mime='text/csv',
)
df = history_data
st.table(df.style.apply(color_status, subset=['Status']))
st.markdown("## Foto Kehadiran")
listAttend = os.listdir(history_path+'/attendance_photo/')
for i in range(0, len(listAttend), 3):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(Image.open(history_path + '/attendance_photo/' + listAttend[i]))
        name = listAttend[i].split('.')
        st.caption(name[0].title())
    if len(listAttend) > (i + 1):
        with col2:
            st.image(Image.open(history_path + '/attendance_photo/' + listAttend[i + 1]))
            name = listAttend[i+1].split('.')
            st.caption(name[0].title())
    if len(listAttend) > (i + 2):
        with col3:
            st.image(Image.open(history_path + '/attendance_photo/' + listAttend[i + 2]))
            name = listAttend[i+2].split('.')
            st.caption(name[0].title())
