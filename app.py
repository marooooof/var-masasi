import streamlit as st
import pandas as pd

# 1. Sayfa Ayarları (Menüyü Gizle)
st.set_page_config(page_title="VAR Masası", page_icon="⚽", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS Tasarım
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    [data-testid="stSidebar"] { display: none; }
    .pozisyon-karti {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        border-left: 6px solid #4CAF50;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .karti-kirmizi { border-left: 6px solid #FF5252 !important; }
    h1, h2, h3, p { color: #ffffff; }
    a { color: #888888 !important; text-decoration: none; }
    a:hover { color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

# --- VERİ ÇEKME FONKSİYONU ---
def verileri_getir():
    # SENİN EXCEL ID'N
