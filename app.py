import streamlit as st
import pandas as pd

# 1. Sayfa Ayarları
st.set_page_config(page_title="VAR Masası - Yorumcu Görüşleri", page_icon="📝", layout="wide")

# Google Sheets URL'si (Değişmedi)
G_SHEET_URL = 'https://docs.google.com/spreadsheets/d/10IDYPgr-8C_xmrWtRrTiG3uXiOYLachV3XjhpGlY1Ug/export?format=csv&gid=82638230'

# Veriyi yükleme fonksiyonu (Zaman Damgasını atıyoruz)
@st.cache_data(ttl=60) 
def load_data(url):
    try:
        df = pd.read_csv(url)
        # Eğer 'Zaman Damgası' sütunu varsa, onu düşür
        if 'Zaman Damgası' in df.columns:
            df = df.drop(columns=['Zaman Damgası'])
        return df
    except Exception as e:
        st.error(f"Veri yüklenirken bir hata oluştu. Lütfen E-Tablonun 'Herkese Açık' olduğundan emin olun.")
        return pd.DataFrame()

# 2. TASARIM KODLARI (FPL Tarzı Koyu Tema)
st.markdown("""
<style>
    /* Genel Arka Plan - Koyu Gri */
    .stApp {
        background-color: #1a202c; /* Koyu laciverte yakın gri */
        color: #e2e8f0; /* Açık gri yazı */
        font-family: 'Inter', sans-serif; /* Modern font */
    }

    /* Başlıklar */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
        font-weight: 700;
        text-align: center;
    }

    /* Genel Konteyner ve Kart Stili */
    .stCard {
        background-color: #2d3748; /* Biraz daha açık gri kartlar */
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        margin-bottom: 15px;
        border
