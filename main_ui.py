import streamlit as st
from PIL import Image

def main():
    st.set_page_config(
        page_title="Welcome"
    )
    st.title("Project Overview")
    st.markdown("***")
    st.markdown("### Face Recognition Atttendance System")
    st.markdown("AI Global Impact Festival Country Winners")
    st.markdown("Dibuat tahun 2021")
    st.markdown("Dibuat Oleh :")
    data_profil_hafizh = """
                - Nama  : Muhammad Hafizh Auliansyah
                - Umur  : 19
                - TTL   : Bandung, 26 April 2003
                - Alumni SMKN 1 Cimahi angkatan 45
                - Mahasiswa **D3-Teknik Informatika** di **Politeknik Negeri Bandung**
            """
    data_profil_gani = """
                    - Nama  : Muhammad Gani Ilham
                    - Umur  : 19
                    - TTL   : Bandar Lampung, 26 April 2003
                    - Alumni SMKN 1 Cimahi angkatan 45
                    - Bekerja di **PT Dasa Aprilindo Sentosa** sebagai **Team Lead of Developer**
                """
    image_hafizh = Image.open("images/ui_images/hafizh.jpg")
    image_gani = Image.open("images/ui_images/gani.jpeg")
    col1, col2 = st.columns(2)
    with col1:
        st.image(image_hafizh)
    with col2:
        st.markdown(data_profil_hafizh)
    col1, col2 = st.columns(2)
    with col1:
        st.image(image_gani)
    with col2:
        st.markdown(data_profil_gani)
