import streamlit as st
import pandas as pd

# 1. Sayfa Ayarları ve Tema
st.set_page_config(page_title="VAR Masası", page_icon="📝", layout="wide")

# Google Sheets'ten veriyi çekeceğimiz URL.
# Bu link, senin Form yanıtlarının düştüğü E-Tablonun CSV formatındaki dışa aktarım linkidir.
G_SHEET_URL = 'https://docs.google.com/spreadsheets/d/10IDYPgr-8C_xmrWtRrTiG3uXiOYLachV3XjhpGlY1Ug/export?format=csv&gid=82638230'

# Streamlit Cache özelliği: Veri değişmedikçe her seferinde Google'dan tekrar çekmez.
@st.cache_data(ttl=60) # 1 dakikada bir (60 saniye) güncellensin.
def load_data(url):
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        # Hata mesajını sadece yönetici görebilir, halk görmez.
        st.error(f"Veri tablosu yüklenemedi. Yönetici: Bağlantıyı kontrol edin.")
        return pd.DataFrame()

# 2. TASARIM KODLARI (Apple Sadeliği)
st.markdown("""
<style>
    .stApp { background-color: #ffffff; color: #333; }
    h1, h2, h3 { font-family: 'Helvetica Neue', sans-serif; color: #1d1d1f; text-align: center; }
    /* Tablo stili */
    .stDataFrame {
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
</style>
""", unsafe_allow_html=True)

# 3. VERİYİ YÜKLE VE GÖSTER
df = load_data(G_SHEET_URL)

st.title("⚽ VAR Masası")
st.markdown("---") # Sadece bir ayırıcı çizgi

# Veri yükleme başarılıysa
if not df.empty:
    
    # "Toplanan Ham Veri" vb. alt başlıklar silindi.
    
    # Veri Tablosu
    st.dataframe(
        df, 
        use_container_width=True, 
        hide_index=True 
    )

    st.markdown("---")
    
else:
    # Veri boşsa (hata varsa) boş bir çizgi görünür.
    pass
