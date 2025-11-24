import streamlit as st
import pandas as pd
import numpy as np

# --- 1. FONKSİYONLAR VE VERİ (AYNI KALIYOR) ---
G_SHEET_URL = 'https://docs.google.com/spreadsheets/d/10IDYPgr-8C_xmrWtRrTiG3uXiOYLachV3XjhpGlY1Ug/export?format=csv&gid=82638230'

def safe_get(df, column_name, default='Gerekçe/Analiz notu mevcut değil.'):
    if df.empty or column_name not in df.columns or df.shape[0] == 0:
        return default
    value = df[column_name].iloc[0]
    if pd.isna(value): return default
    return str(value)

@st.cache_data(ttl=60)
def load_data(url):
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip() 
        if 'Zaman damgası' in df.columns: df = df.drop(columns=['Zaman damgası'])
        return df
    except Exception: return pd.DataFrame()

# 2. TASARIM KODLARI (X/TWITTER GÖRÜNÜMÜ)
st.set_page_config(page_title="VARCast - Gelişmiş Analiz", layout="wide", page_icon="⚽")

# --- YENİ CSS: TAM YUVARLAK KUTULAR ---
st.markdown("""
<style>
    /* Temel PL Renkleri */
    :root {
        --pl-purple: #4A0082; /* PL Logosu Moru */
        --pl-cyan: #00FFFF;   /* Vurgu Turkuazı */
        --pl-dark-base: #12121E; /* Çok Koyu Mor/Mavi Zemin */
        --input-bg: #1A1A22; /* X/Twitter input arka planı */
    }

    /* Genel Arka Plan */
    .stApp {
        background-color: var(--pl-dark-base); 
        color: #EAEAEA; 
        font-family: Arial, sans-serif; 
    }
    
    /* Ana Konteynerlerin Stili (Kartlar) */
    .stContainer, .css-fg4ri0 { 
        background: rgba(27,27,43,0.7);
        backdrop-filter: blur(6px); 
        border-radius: 1rem;
        border: 1px solid rgba(74, 0, 130, 0.5); 
        padding: 2rem;
        margin-bottom: 1rem;
    }
    
    /* Başlıklar */
    h1, h2, h3 { color: #FFFFFF; font-weight: 700; text-align: center; }

    /* 🟢 X/TWITTER STİLİ BURADA BAŞLIYOR 🟢 */

    /* Butonlar: Tam Yuvarlak ve PL Moru */
    .stButton>button {
        background-color: var(--pl-purple); /* PL Moru */
        color: white;
        border-radius: 9999px; /* Kapsül şekli */
        border: none;
        padding: 8px 20px; 
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #5d009b; /* Hafif koyu hover */
        transform: scale(1.02);
    }

    /* Seçim Kutuları (Selectbox): Yuvarlak Input ve Siyah/Koyu Çerçeve */
    .stSelectbox>div>div>div:first-child {
        background-color: var(--input-bg);
        border: 1px solid #333344;
        border-radius: 9999px; /* Tam yuvarlak */
        padding: 4px 15px; /* Daha dolgun görünüm */
        color: #EAEAEA;
    }
    .stSelectbox>label {
        color: #AAAAAA; /* Etiket rengini hafif gri yapalım */
        font-size: 13px;
    }
    
    /* Metin Giriş Kutuları (Aynı stil) */
    .stTextInput>div>div>input {
        background-color: var(--input-bg) !important;
        border: 1px solid #333344 !important;
        border-radius: 9999px !important; /* Tam yuvarlak */
        padding: 8px 15px !important;
        color: #EAEAEA !important;
    }

    /* Etiketler/Statusler */
    .correct-badge { background-color: #38A169 !important; color: white; padding: 5px 10px; border-radius: 9999px; font-size: 14px; }
    .wrong-badge { background-color: #E53E3E !important; color: white; padding: 5px 10px; border-radius: 9999px; font-size: 14px; }
    .neutral-badge { background-color: var(--pl-purple); color: white; padding: 5px 10px; border-radius: 9999px; font-size: 14px; }
    .commentator-card div:first-child { color: var(--pl-cyan); }
    
</style>
""", unsafe_allow_html=True)


# --- 3. ANA UYGULAMA MANTIĞI ---

df = load_data(G_SHEET_URL)

if df.empty:
    st.error("Veri yüklenemedi. Lütfen Google Sheets bağlantısını ve sütun adlarını kontrol edin.")
    st.stop()


# Liste oluşturma fonksiyonları (Kodun geri kalanı aynı)
def extract_teams(match_name):
    try:
        if pd.isna(match_name): return []
        teams = [team.strip() for team in str(match_name).split('-')]
        return teams
    except: return []

all_teams = set()
for match in df['Maç Adı'].dropna().unique(): 
    for team in extract_teams(match):
        if team: all_teams.add(team)
all_teams = sorted(list(all_teams))
all_commentators = sorted(df['Yorumcu'].dropna().unique().tolist()) 
all_referees = sorted(df['Hakem'].dropna().unique().tolist())


# 5. ÇOKLU FİLTRELEME ARAYÜZÜ (Yuvarlak kutular burada görünecek)
st.subheader("🔍 Analiz Filtreleri")
filter_cols = st.columns(3)

with filter_cols[0]:
    selected_team = st.selectbox("⚽ Takımı Seçiniz:", options=['Tümü'] + all_teams, key="team_selector")

with filter_cols[1]:
    selected_commentator = st.selectbox("🎙️ Yorumcuyu Seçiniz:", options=['Tümü'] + all_commentators, key="commentator_selector")

with filter_cols[2]:
    selected_referee = st.selectbox("👤 Hakemi Seçiniz:", options=['Tümü'] + all_referees, key="referee_selector")

# (Kademeli filtreleme mantığı ve layout, performans için aynı kalıyor...)
# ... (Devamı aşağıda, kodun geri kalanı değişmiyor)

# KADEMELİ FİLTRELEME
filtered_df = df.copy()
if selected_team != 'Tümü': filtered_df = filtered_df[filtered_df['Maç Adı'].apply(lambda x: selected_team in extract_teams(x))]
if selected_commentator != 'Tümü': filtered_df = filtered_df[filtered_df['Yorumcu'] == selected_commentator]
if selected_referee != 'Tümü': filtered_df = filtered_df[filtered_df['Hakem'] == selected_referee]
current_analysis_df = filtered_df
position_column_name = 'Olay' 

if current_analysis_df.empty:
    st.info("Seçtiğiniz filtrelere uyan herhangi bir olay bulunamadı.")
    st.stop()

position_list = current_analysis_df[position_column_name].dropna().unique().tolist() 
if not position_list:
    st.info("Seçtiğiniz filtrelere uyan herhangi bir olay bulunamadı.")
    st.stop()

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

ref_decision = safe_get(final_analysis_df, 'Hakem Karar', default='Karar Girilmemiş') 
ref_explanation = safe_get(final_analysis_df, 'Yorum')

# 7. LAYOUT ve GÖRSELLEŞTİRME
st.markdown("---")
col_list = st.columns([1, 2, 1])

# --- SOL SÜTUN (ANALİZ NOTU VE GENEL ORAN) ---
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
                    <div style='font-weight: 600; color: var(--pl-cyan);'>{name}</div>
                    <div>Yorum: {opinion_text}</div>
                    <div style='font-weight: 700;'>Hakemle Aynı Fikirde: {status_emoji}</div>
                </div>
                """, unsafe_allow_html=True
            )
    else:
        st.markdown("<p class='opacity-70'>Bu pozisyon için yorumcu kaydı yok.</p>", unsafe_allow_html=True)
