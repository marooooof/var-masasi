import streamlit as st
import pandas as pd

# 1. Sayfa Ayarları ve Tema
st.set_page_config(page_title="VAR Masası - Yorumcu Verileri", page_icon="📝", layout="wide")

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
        st.error(f"Veri yüklenirken bir hata oluştu. Lütfen E-Tablonun 'Herkese Açık' olduğundan emin olun.")
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
    /* Bilgilendirme kutusu (info) */
    .stInfo {
        background-color: #f2f2f7;
        color: #1d1d1f;
        border: none;
        border-radius: 12px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# 3. VERİYİ YÜKLE VE GÖSTER
df = load_data(G_SHEET_URL)

st.title("⚽ VAR Masası")
st.markdown("<p style='text-align: center; color: #86868b;'>Yorumcu Görüşleri ve Hakem Karşılaştırma Veri Tablosu</p>", unsafe_allow_html=True)
st.markdown("---")

# Veri yükleme başarılıysa
if not df.empty:
    
    # Toplanan Ham Veri yerine sadece Var Masası yazdık.
    st.subheader("Var Masası")
    st.info(f"Sonuçlar şu ana kadar **{len(df)}** farklı görüşü yansıtıyor. Son güncelleme: {pd.Timestamp.now().strftime('%H:%M:%S')}")
    
    # Veri Tablosu
    st.dataframe(
        df, 
        use_container_width=True, 
        hide_index=True 
    )

    st.markdown("---")
    
    st.markdown("<p style='text-align: center; color: #d2d2d7;'>Veriler Google E-Tablolar'dan 1 dakikada bir otomatik çekilmektedir.</p>", unsafe_allow_html=True)

else:
    st.error("Veri tablosu yüklenemiyor. Lütfen E-Tablonun 'Herkese Açık' olduğundan emin olun.")
