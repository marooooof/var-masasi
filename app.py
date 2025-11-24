import streamlit as st

# 1. Sayfa Ayarları
st.set_page_config(page_title="VAR Masası", page_icon="⚽", layout="centered")

# 2. TASARIM KODLARI (Sade ve Şık - Apple Tarzı)
st.markdown("""
<style>
    /* Arka plan ve genel renkler */
    .stApp {
        background-color: #ffffff;
        color: #333333;
    }
    
    /* Başlıklar */
    h1, h2, h3 {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #1d1d1f;
        font-weight: 600;
        text-align: center; /* Başlığı ortala */
    }

    /* Video Link Kutusu */
    .stTextInput>div>div>input {
        border-radius: 12px;
        border: 1px solid #d2d2d7;
        padding: 12px;
        background-color: #f5f5f7;
        color: #333;
        font-size: 16px;
    }

    /* Analiz Butonu (Mavi Hap) */
    .stButton>button {
        background-color: #0071e3;
        color: white;
        border-radius: 980px;
        border: none;
        padding: 12px 30px;
        font-size: 16px;
        font-weight: 500;
        width: 100%; /* Buton tüm satırı kaplasın */
        margin-top: 10px;
    }

    /* Buton efekti */
    .stButton>button:hover {
        background-color: #0077ed;
        transform: scale(1.01);
        box-shadow: 0 4px 12px rgba(0,113,227,0.3);
    }
    
    /* Bilgi mesajları kutusu */
    .stInfo {
        background-color: #f2f2f7;
        color: #1d1d1f;
        border: none;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# 3. EKRAN İÇERİĞİ (Herkes Burayı Görür)

# Üst Başlık
st.title("⚽ VAR Kontrol Merkezi")
st.markdown("<p style='text-align: center; color: #86868b;'>Futbol analiz ve yorumcu özet sistemi</p>", unsafe_allow_html=True)

st.markdown("---")

# Giriş Alanı
col1, col2, col3 = st.columns([1, 10, 1]) # Ortalamak için boşluklu sütunlar
with col2:
    st.info("💡 **Nasıl Kullanılır:** YouTube video linkini aşağıya yapıştırın ve analizi başlatın.")
    
    video_link = st.text_input("Video Linki", placeholder="https://youtube.com/watch?v=...")
    
    if st.button("Analizi Başlat"):
        if video_link:
            st.success(f"Video işleniyor... (Simülasyon): {video_link}")
            # Buraya ileride yapay zeka kodumuz gelecek
        else:
            st.warning("Lütfen önce bir link yapıştırın.")

st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #d2d2d7;'>Powered by Gemini AI</p>", unsafe_allow_html=True)
