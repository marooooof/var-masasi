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
    # Sütun kontrolünü basit yapıyoruz (Hata riskini azaltmak için try-except'i kaldırdım)
    if len(df.columns) >= 7:
        # Sütun İsimlerini Düzenle
        df.columns = ["Zaman", "Maç", "Olay", "Hakem", "Resmi Karar", "Yorumcu", "Durum", "Yorum"] + list(df.columns[8:])
        
        # En yeniyi en üste al
        df = df.iloc[::-1]

        # Pozisyonları Listele
        for index, row in df.iterrows():
            renk_class = "pozisyon-karti"
            # "Katılmıyor" veya "Hayır" içeriyorsa kırmızı yap
            durum_metni = str(row["Durum"])
            if "Katılmıyor" in durum_metni or "Hayır" in durum_metni:
                renk_class += " karti-kirmizi"
            
            html_code = f"""
            <div class="{renk_class}">
                <h3 style="margin:0; color:#fff;">{row['Maç']} <span style="font-size:14px; color:#aaa;">(Hakem: {row['Hakem']})</span></h3>
                <p style="margin-top:5px; color:#ccc;"><i>"{row['Olay']}"</i></p>
                <div style="background-color:rgba(255,255,255,0.1); padding:10px; border-radius:5px; margin-top:10px;">
                    <strong style="color:#FFD700;">{row['Yorumcu']}:</strong> {durum_metni} <br>
                    <span style="font-size:14px; color:#eee;">"{row['Yorum']}"</span>
                </div>
                <p style="font-size:12px; margin-top:5px; text-align:right;">Resmi Karar: <b>{row['Resmi Karar']}</b></p>
            </div>
            """
            st.markdown(html_code, unsafe_allow_html=True)
    else:
        st.warning("Veriler yükleniyor ama formatta sorun var. Sütun sayısı eksik olabilir.")
else:
    st.info("Veriler yükleniyor... (Eğer uzun sürerse Excel 'Paylaş' ayarını kontrol et)")

# --- ALT BİLGİ ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; font-size: 12px; color: #444;">
    VAR Masası © 2025
</div>
""", unsafe_allow_html=True)

# LİNKİNİ BURAYA KOYDUM
form_linki = "https://docs.google.com/forms/d/1du4ImD-UW9ovIr6bkyb0_5rdFy7Bs5WwuFTOJPqjbIY/viewform"
st.caption(f"[Yönetici Girişi]({form_linki})")
