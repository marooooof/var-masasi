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
    SHEET_ID = "10IDYPgr-8C_xmrWtRrTiG3uXiOYLachV3XjhpGlY1Ug"
    
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    try:
        df = pd.read_csv(url)
        return df
    except:
        return pd.DataFrame()

# Verileri Çek
df = verileri_getir()

# --- BAŞLIK ---
c1, c2 = st.columns([1, 15])
with c1:
    st.write("⚽")
with c2:
    st.title("VAR MASASI")

st.markdown("---")

# --- ANA EKRAN ---
if not df.empty:
    try:
        # Sütun İsimleri (Senin form sorularına göre)
        if len(df.columns) >= 7:
            # Sütunları standartlaştır
            df.columns = ["Zaman", "Maç", "Olay", "Hakem", "Resmi Karar", "Yorumcu", "Durum", "Yorum"] + list(df.columns[8:])
            df = df.iloc[::-1] # En yen
