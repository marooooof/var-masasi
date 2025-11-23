import streamlit as st
import pandas as pd

# 1. Sayfa Ayarları (Menüyü Gizle)
st.set_page_config(page_title="VAR Masası", page_icon="⚽", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS Tasarım (Yan menüyü tamamen yok et)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    
    /* Yan Menüyü Komple Gizle */
    [data-testid="stSidebar"] { display: none; }
    
    /* Kart Tasarımı */
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
    
    /* Link Rengi */
    a { color: #888888 !important; text-decoration: none; }
    a:hover { color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

# --- VERİ ÇEKME FONKSİYONU ---
def verileri_getir():
    # --- BURAYI DOLDURMAYI UNUTMA ---
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
        # Sütun İsimleri
        df.columns = ["Zaman", "Maç", "Olay", "Hakem", "Resmi Karar", "Yorumcu", "Durum", "Yorum"]
        df = df.iloc[::-1] # En yeniyi en üste al

        # Pozisyonları Listele
        for index, row in df.iterrows():
            renk_class = "pozisyon-karti"
            if "Hayır" in str(row["Durum"]) or "Katılmıyor" in str(row["Durum"]):
                renk_class += " karti-kirmizi"
            
            html_code = f"""
            <div class="{renk_class}">
                <h3 style="margin:0; color:#fff;">{row['Maç']} <span style="font-size:14px; color:#aaa;">(Hakem: {row['Hakem']})</span></h3>
                <p style="margin-top:5px; color:#ccc;"><i>"{row['Olay']}"</i></p>
                <div style="background-color:rgba(255,255,255,0.1); padding:10px; border-radius:5px; margin-top:10px;">
                    <strong style="color:#FFD700;">{row['Yorumcu']}:</strong> {row['Durum']} <br>
                    <span style="font-size:14px; color:#eee;">"{row['Yorum']}"</span>
                </div>
                <p style="font-size:12px; margin-top:5px; text-align:right;">Resmi Karar: <b>{row['Resmi Karar']}</b></p>
            </div>
            """
            st.markdown(html_code, unsafe_allow_html=True)
            
    except Exception as e:
        st.error("Veri bekleniyor...")
else:
    st.info("Veriler yükleniyor...")

# --- ALT BİLGİ (GİZLİ ADMIN LİNKİ) ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; font-size: 12px; color: #444;">
    VAR Masası © 2025 • Veriler Gerçek Yorumculardan Alınmıştır
</div>
""", unsafe_allow_html=True)

# Admin linkini sayfanın EN ALTINA, çok küçük şekilde koydum.
# Kaybolmasın diye lazım olur. İstersen bu 2 satırı silebilirsin.
form_linki = "https://docs.google.com/forms/d/e/1FAIpQLSfKPW499r0Xdm2qbsVeJ-44lcvG8wZy8A9lBARQcfZF3bvL1g/viewform?usp=header"
st.caption(f"[Yönetici Girişi]({form_linki})")
