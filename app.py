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
        border: 1px solid rgba(255, 255, 255, 0.05); /* Hafif çerçeve */
    }

    /* Başarılı (Yeşil) Kutucuklar/İkonlar */
    .stSuccess {
        background-color: #38a169 !important; /* Koyu yeşil */
        color: white !important;
        border-radius: 8px;
        padding: 5px 10px;
        text-align: center;
        font-weight: 600;
        display: inline-block;
    }

    /* Hatalı/Olumsuz (Kırmızı) Kutucuklar/İkonlar */
    .stError {
        background-color: #e53e3e !important; /* Koyu kırmızı */
        color: white !important;
        border-radius: 8px;
        padding: 5px 10px;
        text-align: center;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Bilgilendirme (Mavi/Gri) Kutucuklar/İkonlar */
    .stInfo {
        background-color: #4299e1 !important; /* FPL tarzı mavi */
        color: white !important;
        border-radius: 8px;
        padding: 5px 10px;
        text-align: center;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Metin giriş kutusu (sade) */
    .stTextInput>div>div>input {
        background-color: #2d3748;
        color: #e2e8f0;
        border-radius: 8px;
        border: 1px solid #4a5568;
        padding: 10px;
    }

    /* Genel buton stili */
    .stButton>button {
        background-color: #4299e1; /* FPL Mavi */
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }

    .stButton>button:hover {
        background-color: #3182ce;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# 3. VERİYİ YÜKLE
df = load_data(G_SHEET_URL)

st.title("⚽ VAR Masası")
st.markdown("<p style='text-align: center; color: #cbd5e0;'>Yorumcuların görüşleri ve hakem kararlarının karşılaştırmalı analizi.</p>", unsafe_allow_html=True)
st.markdown("---")

# Eğer veri başarıyla yüklendiyse, kartlar halinde göster
if not df.empty:
    st.subheader(f"Toplam {len(df)} Farklı Görüş Kaydı") # Toplam kayıt sayısını gösterelim

    # Her bir satır için ayrı bir kart oluşturacağız
    # Pandas iterrows() kullanarak DataFrame'deki her bir satırı geziyoruz
    # Streamlit'in column yapısı ile 3'lü, 2'li veya tekli kartlar gösterebiliriz
    
    num_columns = 3 # Bir satırda kaç kart gösterileceği
    cols = st.columns(num_columns) # Sütunları oluştur
    
    for index, row in df.iterrows():
        # Geçerli kartı hangi sütuna yerleştireceğimizi belirle
        with cols[index % num_columns]: 
            st.markdown(f"<div class='stCard'>", unsafe_allow_html=True)
            st.markdown(f"**Yorumcu:** {row.get('Yorumcu Adı', 'Bilinmiyor')}") # 'Yorumcu Adı' sütununu al
            st.markdown(f"**Maç/Olay:** {row.get('Maç ve Olayı Açıklayın', 'Bilinmiyor')}") # 'Maç ve Olayı Açıklayın' sütununu al
            st.markdown(f"**Yorumcu Kararı:** <span class='stInfo'>{row.get('Yorumcu kararı neydi?', 'Bilinmiyor')}</span>", unsafe_allow_html=True) # Yorumcu kararını mavi kutuda göster
            
            hakem_karari = row.get('Hakem Kararı neydi?', 'Bilinmiyor')
            st.markdown(f"**Hakem Kararı:** <span class='stInfo'>{hakem_karari}</span>", unsafe_allow_html=True) # Hakem kararını mavi kutuda göster
            
            fikir = row.get('Yorumcu Hakemle Aynı Fikirde Miydi?', 'Bilinmiyor')
            
            # Fikre göre renk
