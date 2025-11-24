import streamlit as st
import pandas as pd
import numpy as np # Örnek veri oluşturmak için kullanacağız

# --- 1. FONKSİYONLAR VE VERİ ---

# Google Sheets URL'si (Değişmedi)
G_SHEET_URL = 'https://docs.google.com/spreadsheets/d/10IDYPgr-8C_xmrWtRrTiG3uXiOYLachV3XjhpGlY1Ug/export?format=csv&gid=82638230'

@st.cache_data(ttl=60)
def load_data(url):
    try:
        df = pd.read_csv(url)
        # 'Zaman Damgası' sütununu atıyoruz (Kullanıcı İsteği)
        if 'Zaman Damgası' in df.columns:
            df = df.drop(columns=['Zaman Damgası'])
            
        # Gerekirse veri temizliği: Sütun isimlerini boşluksuz hale getirme
        df.columns = df.columns.str.strip()
        return df
    except Exception:
        return pd.DataFrame()

# --- 2. TASARIM (CSS ENJEKSİYONU) ---
# Senin verdiğin renk kodlarına ve dark mode'a uygun CSS
st.set_page_config(page_title="VARCast - Pozisyon Analiz", layout="wide", page_icon="⚽")

st.markdown("""
<style>
    /* Tailwind renklerini Streamlit'e taşıma */
    .stApp {
        background-color: #0E0E11; /* Genel arka plan */
        color: #EAEAEA; /* Yazı rengi */
        font-family: Arial, sans-serif;
    }
    
    /* Kartların ve Ana Konteynerlerin Stili (Glass/Card Efekti) */
    .stContainer, .css-fg4ri0 { /* Streamlit'in ana konteyner ID'leri */
        background: rgba(17,17,19,0.6); 
        backdrop-filter: blur(6px); /* Glass effect */
        border-radius: 1rem;
        border: 1px solid rgba(34,34,40, 0.5); /* #222228 */
        padding: 2rem;
        margin-bottom: 1rem;
    }
    
    /* Başlıklar */
    h1, h2, h3 { color: #FFFFFF; font-weight: 600; }
    
    /* Butonlar/Etiketler (DEVAM/PENALTI) */
    .correct-badge { background-color: #38A169; color: white; padding: 5px 10px; border-radius: 9999px; font-size: 14px; }
    .wrong-badge { background-color: #E53E3E; color: white; padding: 5px 10px; border-radius: 9999px; font-size: 14px; }
    .neutral-badge { background-color: #2D3748; color: #EAEAEA; padding: 5px 10px; border-radius: 9999px; font-size: 14px; }

    /* Yorumcu Kartları */
    .commentator-card {
        background-color: #121217; /* Biraz daha koyu kart arka planı */
        border-radius: 8px;
        padding: 12px;
        border: 1px solid #1A1A1F;
        margin-bottom: 10px;
    }
    
    /* Sidebar'daki pozisyon arama inputu stili */
    div[data-testid="stSidebar"] input {
        background-color: #121217 !important; 
        border: 1px solid #222228 !important;
        color: #EAEAEA !important;
    }
    
</style>
""", unsafe_allow_html=True)

# --- 3. ANA UYGULAMA MANTIĞI ---

df = load_data(G_SHEET_URL)

if df.empty:
    st.error("Veri yüklenemedi. Lütfen Google Sheets bağlantısını kontrol edin.")
    st.stop()

# 4. POZİSYON SEÇİMİ (HTML'deki listeye Streamlit eşdeğeri)

# Sütun isimlerindeki boşlukları temizlediğimiz için 'Maç ve Olayı Açıklayın' yerine 'MaçveOlayıAçıklayın' kullanacağız.
try:
    position_list = df['Maç ve Olayı Açıklayın'].unique().tolist()
    
    # Varsayılan olarak listedeki ilk öğeyi seçelim
    default_position = position_list[0] if position_list else 'Veri Yok'
    
    # Pozisyonu seçme kutusu (HTML'deki aside/list yerine)
    selected_position = st.selectbox(
        "🔎 Pozisyonu Seçiniz:", 
        options=position_list, 
        index=position_list.index(default_position) if default_position in position_list else 0,
        placeholder="Pozisyon ara...",
        key="position_selector"
    )
    
except KeyError:
    st.error("Hata: Veri tablosunda 'Maç ve Olayı Açıklayın' sütunu bulunamadı.")
    st.stop()

# Seçilen pozisyona ait tüm yorumcu kayıtlarını filtrele
current_analysis_df = df[df['Maç ve Olayı Açıklayın'] == selected_position]

# Hakem kararını al (İlk kayıttan alıyoruz, varsayarak aynı pozisyon için aynıdır)
ref_decision = current_analysis_df['Hakem Kararı neydi?'].iloc[0] if not current_analysis_df.empty else 'Belirtilmemiş'
ref_explanation = current_analysis_df['Analiz Notları'].iloc[0] if 'Analiz Notları' in current_analysis_df.columns and not current_analysis_df.empty else 'Gerekçe mevcut değil.'


# 5. LAYOUT: HTML'deki gibi 3 sütunlu düzeni kur
col_list = st.columns([1, 2, 1])

# --- SOL SÜTUN (POZİSYON LİSTESİ) ---
# Bu alana sadece bir metin bırakıyorum, asıl liste yukarıdaki st.selectbox oldu
with col_list[0]:
    st.markdown(f"**Seçilen Pozisyon:** {selected_position}")
    st.markdown(f"<div class='neutral-badge'>Toplam Kayıt: {len(current_analysis_df)}</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("Pozisyon Notları")
    # Yorumcu listesi seçili olduğu için buraya bir özet koyalım
    st.markdown(f"<p class='text-sm opacity-80'>{ref_explanation[:200]}...</p>", unsafe_allow_html=True)


# --- ORTA SÜTUN (GÖRSEL VE KARAR) ---
with col_list[1]:
    
    # Hakem Kararı Kartı
    with st.container(border=True): # Streamlit konteyneri ile kart görünümü
        st.markdown(f"## 🛎️ Hakem Kararı: {ref_decision}")
        
        # Karar etiketi
        badge_class = 'neutral-badge'
        if ref_decision in ['Penaltı', 'Kırmızı Kart']: badge_class = 'wrong-badge'
        if ref_decision in ['Devam', 'Aut']: badge_class = 'correct-badge' # Varsayım

        st.markdown(f"<div class='{badge_class}'>{ref_decision.upper()}</div>", unsafe_allow_html=True)
        st.markdown(f"<p class='text-sm opacity-80 mt-3'>Gerekçe: {ref_explanation}</p>", unsafe_allow_html=True)

        # İstatistik Barı Hesaplama
        agree_count = current_analysis_df[current_analysis_df['Yorumcu Hakemle Aynı Fikirde Miydi?'] == 'Evet'].shape[0]
        total = len(current_analysis_df)
        agree_percent = round((agree_count / total) * 100) if total > 0 else 0

        st.markdown("---")
        st.markdown(f"**Hakem ile aynı görüşteki yorumcuların oranı:** {agree_percent}%")
        # Basit bir Streamlit barı
        st.progress(agree_percent)

# --- SAĞ SÜTUN (YORUMCULAR) ---
with col_list[2]:
    st.subheader("🎙️ Yorumcu Görüşleri")
    
    if not current_analysis_df.empty:
        for index, row in current_analysis_df.iterrows():
            # Yorumcu kartı (Custom CSS ile)
            name = row.get('Yorumcu Adı', 'Anonim')
            opinion_text = row.get('Yorumcu kararı neydi?', 'Görüş belirtilmemiş.')
            agreed = row.get('Yorumcu Hakemle Aynı Fikirde Miydi?', 'Bilinmiyor') == 'Evet'
            
            # Etiket ve renk
            status_emoji = '✅' if agreed else '❌'
            status_class = 'stSuccess' if agreed else 'stError'
            
            st.markdown(
                f"""
                <div class='commentator-card'>
                    <div class='flex justify-between items-center'>
                        <div style='font-weight: 600; color: #4299e1;'>{name}</div>
                        <div class='{status_class}'>{status_emoji}</div>
                    </div>
                    <div class='text-sm opacity-85 mt-2'>{opinion_text}</div>
                </div>
                """, unsafe_allow_html=True
            )
    else:
        st.markdown("<p class='opacity-70'>Bu pozisyon için henüz yorumcu kaydı yok.</p>", unsafe_allow_html=True)
