import streamlit as st
import pandas as pd

# --- 1. FONKSİYONLAR VE VERİ ---

G_SHEET_URL = 'https://docs.google.com/spreadsheets/d/10IDYPgr-8C_xmrWtRrTiG3uXiOYLachV3XjhpGlY1Ug/export?format=csv&gid=82638230'

@st.cache_data(ttl=60)
def load_data(url):
    try:
        df = pd.read_csv(url)
        
        # 🟢 GİZLİ BOŞLUKLARI TEMİZLEME VE İSİM KONTROLÜ
        df.columns = df.columns.str.strip() 
        
        if 'Zaman damgası' in df.columns:
            df = df.drop(columns=['Zaman damgası'])
            
        return df
    except Exception:
        return pd.DataFrame()

# 2. TASARIM KODLARI (Aynı)
st.set_page_config(page_title="VARCast - Pozisyon Analiz", layout="wide", page_icon="⚽")
st.markdown("""
<style>
    /* ... (CSS KODU AYNI KALIYOR) ... */
    .stApp { background-color: #0E0E11; color: #EAEAEA; font-family: Arial, sans-serif; }
    .stContainer, .css-fg4ri0 { background: rgba(17,17,19,0.6); backdrop-filter: blur(6px); border-radius: 1rem; border: 1px solid rgba(34,34,40, 0.5); padding: 2rem; margin-bottom: 1rem; }
    h1, h2, h3 { color: #FFFFFF; font-weight: 600; text-align: center; }
    .correct-badge { background-color: #38a169 !important; color: white; padding: 5px 10px; border-radius: 9999px; font-size: 14px; }
    .wrong-badge { background-color: #E53E3E !important; color: white; padding: 5px 10px; border-radius: 9999px; font-size: 14px; }
    .commentator-card { background-color: #121217; border-radius: 8px; padding: 12px; border: 1px solid #1A1A1F; margin-bottom: 10px;}
</style>
""", unsafe_allow_html=True)


# --- 3. ANA UYGULAMA MANTIĞI ---

df = load_data(G_SHEET_URL)

if df.empty:
    st.error("Veri yüklenemedi. Lütfen Google Sheets bağlantısını kontrol edin.")
    st.stop()


# 4. POZİSYON SEÇİMİ (ŞİMDİ 'Olay' SÜTUNUNU KULLANIYORUZ)
try:
    position_column_name = 'Olay' # 👈 Düzeltme yapıldı
    position_list = df[position_column_name].unique().tolist()
    default_position = position_list[0] if position_list else 'Veri Yok'
    
    selected_position = st.selectbox(
        "🔎 Pozisyonu Seçiniz:", 
        options=position_list, 
        index=position_list.index(default_position) if default_position in position_list else 0,
        placeholder="Pozisyon ara...",
        key="position_selector"
    )
    
except KeyError:
    # Bu hata gelirse, 'Olay' sütununu da yanlış girmişsin demektir.
    st.error("Çok kritik bir hata: 'Olay' sütunu da bulunamıyor. Lütfen E-Tablonuzdaki pozisyon başlığı sütun adını tekrar kontrol edin.")
    st.stop()


# Seçilen pozisyona ait tüm yorumcu kayıtlarını filtrele
current_analysis_df = df[df[position_column_name] == selected_position]

# Hakem kararını al (ŞİMDİ 'Hakem Karar' SÜTUNUNU KULLANIYORUZ)
ref_decision = current_analysis_df['Hakem Karar'].iloc[0] if not current_analysis_df.empty else 'Belirtilmemiş'
ref_explanation = current_analysis_df['Yorum'].iloc[0] if 'Yorum' in df.columns and not current_analysis_df.empty else 'Gerekçe/Analiz notu mevcut değil.' # 'Yorum' sütununu gerekçe olarak kullandık


# 5. LAYOUT: 3 sütunlu düzeni kur
col_list = st.columns([1, 2, 1])

# --- SOL SÜTUN (KODDA DİĞER KISIMLAR DEĞİŞMİYOR) ---
with col_list[0]:
    st.markdown(f"**Seçilen Pozisyon:** {selected_position}")
    st.markdown(f"<div class='neutral-badge'>Toplam Kayıt: {len(current_analysis_df)}</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("Analiz Notu")
    st.markdown(f"<p class='text-sm opacity-80'>{ref_explanation[:200]}...</p>", unsafe_allow_html=True)


# --- ORTA SÜTUN (KARAR VE İSTATİSTİK) ---
with col_list[1]:
    with st.container(border=True): 
        st.markdown(f"## 🛎️ Hakem Kararı: {ref_decision}")
        
        # Karar etiketi
        badge_class = 'neutral-badge'
        if ref_decision in ['Penaltı', 'Kırmızı Kart']: badge_class = 'wrong-badge'
        if ref_decision in ['Devam', 'Aut']: badge_class = 'correct-badge'

        st.markdown(f"<div class='{badge_class}'>{ref_decision.upper()}</div>", unsafe_allow_html=True)
        st.markdown(f"<p class='text-sm opacity-80 mt-3'>Gerekçe: {ref_explanation}</p>", unsafe_allow_html=True)

        # İstatistik Barı Hesaplama (ŞİMDİ '6. sütun' KULLANIYORUZ)
        # Assuming '6. sütun' contains 'Evet' veya 'Hayır'
        agree_count = current_analysis_df[current_analysis_df['6. sütun'] == 'Evet'].shape[0]
        total = len(current_analysis_df)
        agree_percent = round((agree_count / total) * 100) if total > 0 else 0

        st.markdown("---")
        st.markdown(f"**Hakem ile aynı görüşteki yorumcuların oranı:** {agree_percent}%")
        st.progress(agree_percent)

# --- SAĞ SÜTUN (YORUMCULAR) ---
with col_list[2]:
    st.subheader("🎙️ Yorumcu Görüşleri")
    
    if not current_analysis_df.empty:
        for index, row in current_analysis_df.iterrows():
            # SÜTUN İSİMLERİ DÜZELTİLDİ: 'Yorumcu' ve '6. sütun'
            name = row.get('Yorumcu', 'Anonim')
            opinion_text = row.get('Yorum', 'Görüş belirtilmemiş.')
            agreed = row.get('6. sütun', 'Bilinmiyor') == 'Evet'
            
            status_emoji = '✅' if agreed else '❌'
            status_class = 'stSuccess' if agreed else 'stError'
            
            st.markdown(
                f"""
                <div class='commentator-card'>
                    <div style='font-weight: 600; color: #4299e1;'>{name}</div>
                    <div class='{status_class}'>{status_emoji}</div>
                    <div class='text-sm opacity-85 mt-2'>{opinion_text}</div>
                </div>
                """, unsafe_allow_html=True
            )
    else:
        st.markdown("<p class='opacity-70'>Bu pozisyon için henüz yorumcu kaydı yok.</p>", unsafe_allow_html=True)
