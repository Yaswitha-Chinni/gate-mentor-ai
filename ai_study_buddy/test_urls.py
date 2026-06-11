import streamlit as st
import json

pg = st.navigation([st.Page('views/home.py', url_path='pdf_summarizer')])
for p in pg.pages:
    print("PAGE:", p.url_path)
