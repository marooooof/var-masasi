import streamlit as st
import pandas as pd

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="VAR Masası", layout="wide", page_icon="⚽")

G_SHEET_URL = 'https://docs.google.com/spreadsheets/d/10IDYPgr-8C_xmrWtRrTiG3uXiOYLachV3XjhpGlY1Ug/export?format=csv&gid=82638230'

# --- 2. FONKSİYONLAR ---
if 'selected_pos_name' not in st.session_state:
    st.session_state.selected_pos_name = None

def safe_get(df, column_name, default='-'):
    if df.empty or column_name not in df.columns or df.shape[0] == 0: return default
    val = df[column_name].iloc[0]
    return default if pd.isna(val) else str(val)

@st.cache_data(ttl=60)
def load_data(url):
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        if 'Zaman damgası' in df.columns: df = df.drop(columns=['Zaman damgası'])
        return df
    except: return pd.DataFrame()

df = load_data(G_SHEET_URL)

# İlk Yükleme Mantığı
if not df.empty and st.session_state.selected_pos_name is None:
    valid_events = df['Olay'].dropna().unique().tolist()
    if valid_events:
        st.session_state.selected_pos_name = valid_events[0]

# --- 3. CSS TASARIM ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    :root {
        --bg-color: #0E0E11;
        --card-bg: #151518;
        --card-border: #222226;
        --accent-green: #00FF85;
        --text-white: #FFFFFF;
        --text-muted: #9CA3AF;
    }

    .stApp { background-color: var(--bg-color); font-family: 'Inter', sans-serif; color: var(--text-white); }
    header { visibility: hidden; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

    /* HEADER */
    .header-logo {
        width: 40px; height: 40px;
        background: linear-gradient(135deg, #00FF85 0%, #0094FF 100%);
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-weight: 800; color: white; font-size: 14px;
    }
    .header-title { font-size: 20px; font-weight: 700; color: white; letter-spacing: -0.5px; }

    /* ARAMA KUTUSU */
    .stTextInput { width: 300px; float: right; }
    .stTextInput > div > div > input {
        background-color: #1F1F23 !important;
        color: #EAEAEA !important;
        border: 1px solid #333 !important;
        border-radius: 99px !important;
        padding: 10px 20px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--accent-green) !important;
        box-shadow: 0 0 0 1px var(--accent-green) !important;
    }

    /* SOL MENÜ */
    div.stButton > button {
        width: 100%;
        background-color: var(--card-bg);
        border: 1px solid var(--card-border);
        color: var(--text-white);
        border-radius: 12px;
        text-align: left;
        padding: 16px 20px;
        font-weight: 600;
        margin-bottom: 8px;
        transition: all 0.2s;
        display: flex; flex-direction: column; align-items: flex-start;
    }
    div.stButton > button:hover {
        border-color: var(--accent-green);
        color: var(--accent-green);
    }
    
    /* ORTA ALAN */
    .main-card {
        background-color: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 20px;
        overflow: hidden;
        padding-bottom: 20px;
    }
    /* Resim Kutusu: Sabit yükseklik + Siyah Arka Plan */
    .image-box {
        width: 100%;
        height: 300px; /* SABİT YÜKSEKLİK - ASLA KAYMAZ */
        background-color: #000; /* Kenarlarda boşluk kalırsa siyah görünsün */
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }
    
    .floating-badge {
        position: absolute; top: 20px; left: 20px;
        background-color: #4B0082; color: white;
        padding: 6px 16px; border-radius: 99px;
        font-size: 12px; font-weight: 700;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        z-index: 5;
    }
    .decision-pill {
        background-color: var(--accent-green);
        color: black;
        display: inline-flex; align-items: center; gap: 8px;
        padding: 10px 24px; border-radius: 99px;
        font-weight: 800; font-size: 14px; text-transform: uppercase;
        margin-top: -45px; margin-left: 25px; position: relative; z-index: 10;
        box-shadow: 0 4px 15px rgba(0, 255, 133, 0.2);
    }
    .content-area { padding: 25px; padding-top: 0; margin-top: 15px; }
    .section-title { font-size: 18px; font-weight: 700; margin-bottom: 10px; color: white; }
    .desc-text { font-size: 14px; line-height: 1.6; color: var(--text-muted); margin-bottom: 25px; }
    .progress-track { background: #2A2A2F; height: 8px; border-radius: 99px; width: 100%; margin-top: 10px; }
    .progress-bar { height: 100%; background: var(--accent-green); border-radius: 99px; }
    .stat-row { display: flex; justify-content: space-between; font-size: 13px; font-weight: 600; margin-top: 5px; color: #777; }
    .analysis-box {
        background-color: #1A1A1D;
        border: 1px solid #2A2A2F;
        border-radius: 12px;
        padding: 15px;
        margin-top: 20px;
    }
    .analysis-header { color: var(--accent-green); font-weight: 600; font-size: 14px; margin-bottom: 5px; display: flex; align-items: center; gap: 6px;}

    /* SAĞ ALAN */
    .commentator-card {
        background-color: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        display: flex; gap: 12px; align-items: flex-start;
    }
    .avatar { width: 40px; height: 40px; border-radius: 50%; object-fit: cover; }
    .status-icon { width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; margin-left: auto; }
    .check { background: var(--accent-green); color: black; }
    .cross { background: #E53E3E; color: white; }

</style>
""", unsafe_allow_html=True)

# --- HEADER KISMI ---
c1, c2 = st.columns([1, 1]) 
with c1:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:20px;">
        <div class="header-logo">VM</div>
        <div class="header-title">VAR Masası</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    col_spacer, col_search = st.columns([1, 2]) 
    with col_search:
        search_query = st.text_input("ara", placeholder="Pozisyon ara...", label_visibility="collapsed")

# --- GRID YAPISI ---
col_left, col_center, col_right = st.columns([3, 6, 3])

# ================= SOL KOLON: LİSTE =================
with col_left:
    st.markdown('<div style="font-weight:700; margin-bottom:15px; color:#fff;">≡ Pozisyon Listesi</div>', unsafe_allow_html=True)
    
    if not df.empty:
        all_events = df['Olay'].dropna().unique()
        # Arama Filtresi
        if search_query:
            events_to_show = [e for e in all_events if search_query.lower() in str(e).lower()]
        else:
            events_to_show = all_events

        for event in events_to_show:
            is_active = (event == st.session_state.selected_pos_name)
            
            if is_active:
                # Aktif buton stili
                st.markdown(f"""<style>div.stButton > button[data-testid="baseButton-secondary"] {{ border-color: #333; }} div.stButton > button:focus {{ background-color: #151518 !important; color:white !important; border-color: #00FF85 !important; }}</style>""", unsafe_allow_html=True)
                label_text = f"🟢 {event}"
            else:
                label_text = event

            if st.button(label_text, key=f"btn_{event}", use_container_width=True):
                st.session_state.selected_pos_name = event
                st.rerun()

# ================= ORTA KOLON: DETAY =================
with col_center:
    if st.session_state.selected_pos_name and not df.empty:
        selected_pos = st.session_state.selected_pos_name
        filtered_df = df[df['Olay'] == selected_pos]
        
        ref_decision = safe_get(filtered_df, 'Hakem Karar')
        ref_note = safe_get(filtered_df, 'Yorum')
        match_name = safe_get(filtered_df, 'Maç Adı', 'Bilinmiyor')
        
        # --- GÖRSEL SEÇİMİ ---
        custom_image = safe_get(filtered_df, 'Görsel', '-')
        if custom_image != '-' and custom_image.startswith('http'):
            main_image_url = custom_image
        else:
            # Varsayılan stadyum görseli
            main_image_url = "https://images.unsplash.com/photo-1522778119026-d647f0565c6a?auto=format&fit=crop&w=800&q=80"
        # ---------------------

        decision_text = str(ref_decision).upper()
        badge_style = "background-color: #333; color: white;"
        icon = "⚖️"
        
        if "penaltı" in decision_text.lower(): 
            badge_style = "background-color: #00FF85; color: black;"
            icon = "✅"
        elif "iptal" in decision_text.lower() or "kırmızı" in decision_text.lower():
            badge_style = "background-color: #E53E3E; color: white;"
            icon = "🛑"

        agree_count = filtered_df[filtered_df['6. sütun'] == 'Evet'].shape[0]
        total = len(filtered_df)
        percent = round((agree_count/total)*100) if total > 0 else 0

        # HTML KART (CONTAIN MODU + SABİT YÜKSEKLİK)
        html_code = f"""
<div class="main-card">
    <div class="image-box">
        <img src="{main_image_url}" style="width: 100%; height: 100%; object-fit: contain; display: block;">
        <div class="floating-badge" style="top: 15px; left: 15px;">Var İncelemesi</div>
    </div>

    <div style="{badge_style}" class="decision-pill">
        {icon} {decision_text}
    </div>

    <div class="content-area">
        <div class="section-title">Hakem Kararı</div>
        <div class="desc-text">
            Ceza sahası içerisinde <b>{match_name}</b> maçında yaşanan bu pozisyonda hakem kararı <b>{ref_decision}</b> yönünde olmuştur.
        </div>
        
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
            <span style="font-weight:700; font-size:14px;">Kamuoyu Görüşü</span>
            <span style="color:#00FF85; font-weight:700;">{percent}%</span>
        </div>
        <div class="progress-track">
            <div class="progress-bar" style="width: {percent}%;"></div>
        </div>
        <div class="stat-row">
            <span>Katılıyor</span>
            <span>Katılmıyor</span>
        </div>
        
        <div class="analysis-box">
            <div class="analysis-header">📄 Analiz Notu</div>
            <div style="font-size:13px; color:#A0A0A0; line-height:1.5;">
                {ref_note}
            </div>
        </div>
    </div>
</div>
"""
        st.markdown(html_code, unsafe_allow_html=True)
        
    else:
        st.info("Bir pozisyon seçiniz.")

# ================= SAĞ KOLON: YORUMCULAR =================
with col_right:
    st.markdown('<div style="font-weight:700; margin-bottom:15px; color:#fff;">💬 Yorumcu Görüşleri</div>', unsafe_allow_html=True)
    
    if st.session_state.selected_pos_name and not df.empty:
        for index, row in filtered_df.iterrows():
            y_isim = safe_get(pd.DataFrame([row]), 'Yorumcu', 'Anonim')
            y_yorum = safe_get(pd.DataFrame([row]), 'Yorum', '-')
            y_fikir = safe_get(pd.DataFrame([row]), '6. sütun', 'Hayır')
            
            if y_fikir == 'Evet':
                icon_class = "check"; icon_symbol = "✔"
            else:
                icon_class = "cross"; icon_symbol = "✖"
            
            avatar_url = f"https://i.pravatar.cc/100?u={index+10}"

            commentator_html = f"""
<div class="commentator-card">
<img src="{avatar_url}" class="avatar">
<div style="flex:1;">
<div style="font-weight:600; font-size:14px; margin-bottom:4px;">{y_isim}</div>
<div style="font-size:12px; color:#9CA3AF; line-height:1.3;">"{y_yorum[:90]}..."</div>
</div>
<div class="status-icon {icon_class}">{icon_symbol}</div>
</div>
"""
            st.markdown(commentator_html, unsafe_allow_html=True)
