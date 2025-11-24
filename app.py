import streamlit as st
import pandas as pd # Veriyi okumak için Pandas'ı kullanıyoruz

# 1. Sayfa Ayarları ve Tema
st.set_page_config(page_title="VAR Masası - Anket Sonuçları", page_icon="📝", layout="wide")

# Google Sheets'ten veriyi çekeceğimiz URL.
# Bu link, senin Form yanıtlarının düştüğü E-Tablonun CSV formatındaki dışa aktarım linkidir.
# E-Tablo ID'si: 10IDYPgr-8C_xmrWtRrTiG3uXiOYLachV3XjhpGlY1Ug
# Sayfa ID'si (GID): 82638230
G_SHEET_URL = 'https://docs.google.com/spreadsheets/d/10IDYPgr-8C_xmrWtRrTiG3uXiOYLachV3XjhpGlY1Ug/export?format=csv&gid=82638230'

# Streamlit Cache özelliği: Veri değişmedikçe her seferinde Google'dan tekrar çekmez.
@st.cache_data(ttl=60) # 1 dakikada bir (60 saniye) güncellensin ki anket sonuçları hızlı düşsün.
def load_data(url):
    try:
        # URL'den veriyi oku ve Pandas DataFrame'e çevir
        df = pd.read_csv(url)
        return df
    except Exception as e:
        # Hata olursa boş bir DataFrame döndür
        st.error(f"Veri yüklenirken bir hata oluştu. E-Tablonun 'Herkese Açık' olduğundan emin olun.")
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

st.title("📝 VAR Masası - Canlı Anket Sonuçları")
st.markdown("<p style='text-align: center; color: #86868b;'>Google Form yanıtları otomatik olarak burada gösteriliyor.</p>", unsafe_allow_html=True)
st.markdown("---")

# Veri yükleme başarılıysa
if not df.empty:
    
    # Anket sonuçlarını daha güzel göstermek için DataFrame'i kullanıyoruz:
    
    # 1. Anketin Başlıkları (Soru Başlıkları)
    st.subheader("📋 Toplanan Ham Veri")
    st.info(f"Toplam **{len(df)}** kişi ankete katıldı. Son güncelleme: {pd.Timestamp.now().strftime('%H:%M:%S')}")
    
    # 2. Veri Tablosu
    st.dataframe(
        df, 
        use_container_width=True, 
        hide_index=True 
    )

    st.markdown("---")
    
    # (Opsiyonel) Eğer istersen, en çok oy alan seçeneği falan burada gösterebiliriz.
    
    st.markdown("<p style='text-align: center; color: #d2d2d7;'>Sonuçlar 1 dakikada bir otomatik güncellenmektedir.</p>", unsafe_allow_html=True)

else:
    st.error("Veri tablosu yüklenemiyor. Lütfen Google E-Tablonun 'Herkese Açık' olduğundan emin olun.")
