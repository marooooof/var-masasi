import streamlit as st
import pandas as pd
import numpy as np

# --- 1. FONKSİYONLAR VE VERİ ---
G_SHEET_URL = 'https://docs.google.com/spreadsheets/d/10IDYPgr-8C_xmrWtRrTiG3uXiOYLachV3XjhpGlY1Ug/export?format=csv&gid=82638230'

# Emniyet Fonksiyonları (safe_get ve load_data aynı kalıyor)
def safe_get(df, column_name, default='Gerekçe/Analiz notu mevcut değil.'):
    if df.empty or column_name not in df.columns or df.shape[0] == 0:
        return default
    
    value = df[column_name].iloc[0]
    if pd.isna(value): # Boş (NaN) kontrolü
        return default
    return str(value)

@st.cache_data(ttl=60)
def load_data(url):
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip() 
        if 'Zaman damgası' in df.columns:
            df = df.drop(columns=['Zaman damgası'])
        return df
    except Exception:
        return pd.DataFrame()

# 2. TASARIM KODLARI
st.set_page_config(page_title="VARCast - Gelişmiş Analiz", layout="wide", page_icon="⚽")
st.markdown("""
<style>
    .stApp { background-color: #0E0E11; color: #EAEAEA; font-family: Arial, sans-serif; }
    .stContainer, .css-fg4ri0 { background: rgba(17,17,19,0.6); backdrop-filter: blur(6px); border-radius: 1rem; border: 1px solid rgba(34,34,40, 0.5); padding: 2rem; margin-bottom: 1rem; }
    h1, h2, h3 { color: #FFFFFF; font-weight: 600; text-align: center; }
    .correct-badge { background-color: #38a169 !important; color: white; padding: 5px 10px; border-radius: 9999px; font-size: 14px; }
    .wrong-badge { background-color: #E53E3E !important; color: white; padding: 5px 10px; border-radius: 9999px; font-size: 14px; }
    .commentator-card { 
        background-color: #121217; border-radius: 8px; padding: 12px; border: 1px solid #1A1A1F; margin-bottom: 10px;
        display: flex; flex-direction: column; gap: 5px;
    }
</style>
""", unsafe_allow_html=True)


# --- 3. ANA UYGULAMA MANTIĞI ---

df = load_data(G_SHEET_URL)

if df.empty:
    st.error("Veri yüklenemedi. Lütfen Google Sheets bağlantısını ve sütun adlarını kontrol edin.")
    st.stop()


# Maç Adı sütununu takımlara ayırma (Bu fonksiyon NaN değerleri görmezden gelir)
def extract_teams(match_name):
    try:
        # Maç Adı'nın NaN olmadığını kontrol et
        if pd.isna(match_name):
            return []
        teams = [team.strip() for team in str(match_name).split('-')]
        return teams
    except:
        return []

# 4. TÜM LİSTELERİ OLUŞTURMA (NaN/TypeError Düzeltmeleri Uygulandı)
all_teams = set()
# Maç Adı sütunundaki boş satırları atıyoruz (dropna())
for match in df['Maç Adı'].dropna().unique(): 
    for team in extract_teams(match):
        if team:
            all_teams.add(team)

all_teams = sorted(list(all_teams))

# 🟢 HATA ÇÖZÜMÜ: Yorumcu ve Hakem listelerini oluştururken boş (NaN) değerleri at
all_commentators = sorted(df['Yorumcu'].dropna().unique().tolist()) 
all_referees = sorted(df['Hakem'].dropna().unique().tolist())


# 5. ÇOKLU FİLTRELEME ARAYÜZÜ
st.subheader("🔍 Analiz Filtreleri")
filter_cols = st.columns(3)

with filter_cols[0]:
    selected_team = st.selectbox(
        "⚽ Takımı Seçiniz:", 
        options=['Tümü'] + all_teams, 
        placeholder="Takım ara...",
        key="team_selector"
    )

with filter_cols[1]:
    selected_commentator = st.selectbox(
        "🎙️ Yorumcuyu Seçiniz:", 
        options=['Tümü'] + all_commentators, 
        placeholder="Yorumcu ara...",
        key="commentator_selector"
    )

with filter_cols[2]:
    selected_referee = st.selectbox(
        "👤 Hakemi Seçiniz:", 
        options=['Tümü'] + all_referees, 
        placeholder="Hakem ara...",
        key="referee_selector"
    )

# 6. KADEMELİ FİLTRELEME MANTIĞI
filtered_df = df.copy()

# 1. Takım Filtresi
if selected_team != 'Tümü':
    filtered_df = filtered_df[filtered_df['Maç Adı'].apply(lambda x: selected_team in extract_teams(x))]

# 2. Yorumcu Filtresi
if selected_commentator != 'Tümü':
    filtered_df = filtered_df[filtered_df['Yorumcu'] == selected_commentator]

# 3. Hakem Filtresi
if selected_referee != 'Tümü':
    filtered_df = filtered_df[filtered_df['Hakem'] == selected_referee]

current_analysis_df = filtered_df

position_column_name = 'Olay' 

if current_analysis_df.empty:
    st.info("Seçtiğiniz filtrelere uyan herhangi bir olay bulunamadı.")
    st.stop()

# Son pozisyon seçimi
position_list = current_analysis_df[position_column_name].unique().tolist()
default_position = position_list[0] if position_list else 'Veri Yok'

st.markdown("---")
selected_position = st.selectbox(
    "📝 Analiz Edilecek Pozisyonu Seçiniz:", 
    options=position_list, 
    index=position_list.index(default_position) if default_position in position_list else 0,
    placeholder="Pozisyon ara...",
    key="position_analyzer"
)

# Son filtreden sonraki veri
final_analysis_df = current_analysis_df[current_analysis_df['Olay'] == selected_position]

# Çekilecek tekil bilgiler
ref_decision = safe_get(final_analysis_df, 'Hakem Karar', default='Karar Girilmemiş') 
ref_explanation = safe_get(final_analysis_df, 'Yorum')


# 7. LAYOUT ve GÖRSELLEŞTİRME
st.markdown("---")
col_list = st.columns([1, 2, 1])

# --- SOL SÜTUN (ANALİZ NOTU) ---
with col_list[0]:
    st.markdown(f"**Seçilen Pozisyon:** {selected_position}")
    st.markdown(f"<div class='neutral-badge'>Toplam Yorumcu Kaydı: {len(final_analysis_df)}</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("Analiz Notu")
    st.markdown(f"<p class='text-sm opacity-80'>{ref_explanation[:200]}...</p>", unsafe_allow_html=True)

    # Genel Oran
    agree_count_all = current_analysis_df[current_analysis_df['6. sütun'] == 'Evet'].shape[0]
    total_count_all = len(current_analysis_df)
    overall_agree_percent = round((agree_count_all / total_count_all) * 100) if total_count_all > 0 else 0

    st.markdown("---")
    st.subheader("Genel Oran")
    st.markdown(f"**Filtrelenmiş Kayıtlarda** Hakemle Aynı Görüş Oranı: **{overall_agree_percent}%**")
    st.progress(overall_agree_percent / 100)


# --- ORTA SÜTUN (KARAR VE İSTATİSTİK) ---
with col_list[1]:
    with st.container(border=True): 
        st.markdown(f"## 🛎️ Hakem Kararı: {ref_decision}")
        
        badge_class = 'neutral-badge'
        if ref_decision in ['Penaltı', 'Kırmızı Kart']: badge_class = 'wrong-badge'
        if ref_decision in ['Devam', 'Aut']: badge_class = 'correct-badge'

        st.markdown(f"<div class='{badge_class}'>{ref_decision.upper()}</div>", unsafe_allow_html=True)
        st.markdown(f"<p class='text-sm opacity-80 mt-3'>Gerekçe: {ref_explanation}</p>", unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("Pozisyona Özel İstatistik")
        
        agree_count_pos = final_analysis_df[final_analysis_df['6. sütun'] == 'Evet'].shape[0]
        total_count_pos = len(final_analysis_df)
        agree_percent_pos = round((agree_count_pos / total_count_pos) * 100) if total_count_pos > 0 else 0

        st.markdown(f"**Bu pozisyonda** Hakemle Aynı Görüşteki Yorumcu Oranı: **{agree_percent_pos}%**")
        st.progress(agree_percent_pos / 100)

# --- SAĞ SÜTUN (YORUMCULAR) ---
with col_list[2]:
    st.subheader("🎙️ Yorumcu Görüşleri")
    
    if not final_analysis_df.empty:
        for index, row in final_analysis_df.iterrows():
            name = row.get('Yorumcu', 'Anonim')
            opinion_text = row.get('Yorum', 'Görüş belirtilmemiş.')
            agreed = row.get('6. sütun', 'Bilinmiyor') == 'Evet'
            
            status_emoji = '✅' if agreed else '❌'
            
            st.markdown(
                f"""
                <div class='commentator-card'>
                    <div style='font-weight: 600; color: #4299e1;'>{name}</div>
                    <div>Yorum: {opinion_text}</div>
                    <div style='font-weight: 700;'>Hakemle Aynı Fikirde: {status_emoji}</div>
                </div>
                """, unsafe_allow_html=True
            )
    else:
        st.markdown("<p class='opacity-70'>Bu pozisyon için yorumcu kaydı yok.</p>", unsafe_allow_html=True)
