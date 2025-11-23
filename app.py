import streamlit as st
import pandas as pd

# 1. Sayfa Ayarları
st.set_page_config(page_title="VAR Masası", page_icon="⚽", layout="wide")

# 2. CSS Tasarım
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
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
    </style>
""", unsafe_allow_html=True)

# --- BAŞLIK ---
st.title("⚽ VAR MASASI")
st.markdown("*Google Form Destekli Canlı Veri Tabanı*")

# --- VERİ ÇEKME FONKSİYONU ---
def verileri_getir():
    # BURAYA KENDİ ID'Nİ YAZACAKSIN (Aşağıdaki tırnakların içine)
    SHEET_ID = "BURAYA_O_KARISIK_HARFLERI_YAPISTIR" 
    
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    try:
        df = pd.read_csv(url)
        return df
    except:
        return pd.DataFrame() # Hata olursa boş tablo dön

# Verileri Çek
df = verileri_getir()

# --- YAN MENÜ (FORM LİNKİ) ---
with st.sidebar:
    st.header("Yönetici Girişi")
    st.info("Veri girmek için aşağıdaki butona tıkla ve formu doldur.")
    
    # 10IDYPgr-8C_xmrWtRrTiG3uXiOYLachV3XjhpGlY1Ug
    form_linki = "https://forms.gle/SENIN_FORM_LINKIN"
    st.link_button("📝 Yeni Veri Gir (Google Form)", form_linki)
    
    if st.button("Verileri Yenile 🔄"):
        st.rerun()

# --- ANA EKRAN ---
if not df.empty:
    # Google Form sütun isimleri bazen uzun olur, onları düzeltelim
    # Senin formundaki sorulara göre burası değişebilir, ama genelde sırayla gelir.
    # Sütun isimlerini kendi kafamıza göre yeniden adlandıralım:
    try:
        df.columns = ["Zaman", "Maç", "Olay", "Hakem", "Resmi Karar", "Yorumcu", "Durum", "Yorum"]
        
        # En yeni en üstte görünsün diye ters çevir
        df = df.iloc[::-1]

        st.subheader(f"🔥 Güncel Gündem ({len(df)} Pozisyon)")
        
        for index, row in df.iterrows():
            # Renk Ayarı
            renk_class = "pozisyon-karti"
            # Formda "Hayır" seçilirse kırmızı olsun
            if "Hayır" in str(row["Durum"]) or "Katılmıyor" in str(row["Durum"]):
                renk_class += " karti-kirmizi"
            
            html_code = f"""
            <div class="{renk_class}">
                <h3 style="margin:0; color:#fff;">{row['Maç']} <span style="font-size:14px; color:#aaa;">(Hakem: {row['Hakem']})</span></h3>
                <p style="margin-top:5px; color:#ccc;"><i>"{row['Olay']}"</i></p>
                <div style="background-color:rgba(255,255,255,0.1); padding:10px; border-radius:5px; margin-top:10px;">
                    <strong style="color:#FFD700;">{row['Yorumcu']} Diyor ki:</strong><br>
                    <span style="font-size:18px;">{row['Durum']}</span> - {row['Yorum']}
                </div>
                <p style="font-size:12px; margin-top:5px; text-align:right;">Resmi Karar: <b>{row['Resmi Karar']}</b></p>
            </div>
            """
            st.markdown(html_code, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Sütun isimleri uyuşmadı, lütfen form sorularını kontrol et. Hata: {e}")
        st.dataframe(df) # Hata olursa ham tabloyu göster
else:
    st.warning("Henüz hiç veri girilmemiş veya Excel bağlantısı hatalı.")
