import streamlit as st

st.title("Capture Settings")
st.markdown("***")

jedaOption = ('1 detik', '10 detik', '1 menit', "5 menit", "10 menit")
jedaUnknown = st.selectbox(
    "Jeda simpan foto wajah tidak dikenal : ", jedaOption
    )

if jedaUnknown == jedaOption[0]:
    st.session_state["unknownPause"] = 1
elif jedaUnknown == jedaOption[1]:
    st.session_state["unknownPause"] = 10
elif jedaUnknown == jedaOption[2]:
    st.session_state["unknownPause"] = 60
elif jedaUnknown == jedaOption[3]:
    st.session_state["unknownPause"] = 300
elif jedaUnknown == jedaOption[4]:
    st.session_state["unknownPause"] = 600

masukOption = ('06:00', '07:00', '08:00', "09:00", "10:00")
jamMasuk = st.selectbox(
    "Pilih waktu masuk : ", masukOption
    )

if jamMasuk == masukOption[0]:
    st.session_state['jamMasuk'] = 6
elif jamMasuk == masukOption[1]:
    st.session_state['jamMasuk'] = 7
elif jamMasuk == masukOption[2]:
    st.session_state['jamMasuk'] = 8
elif jamMasuk == masukOption[3]:
    st.session_state['jamMasuk'] = 9
elif jamMasuk == masukOption[4]:
    st.session_state['jamMasuk'] = 10
