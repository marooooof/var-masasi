import streamlit as st
import pandas as pd

# --- 1. AYARLAR VE DATA ---
st.set_page_config(page_title="VAR Masası", layout="wide", page_icon="⚽")

G_SHEET_URL = 'https://docs.google.com/spreadsheets/d/10IDYPgr-8C_xmrWtRrTiG3uXiOYLachV3XjhpGlY1Ug/export?format=csv&gid=82638230'

# Session State (Seçili pozisyonu hafızada tutar)
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

# İlk Yükleme: Eğer seçim yoksa listenin ilkini seç
if not df.empty and st.session_state.selected_pos_name is None:
    valid_events = df['Olay'].dropna().unique().tolist()
    if valid_events:
        st.session_state.selected_pos_name = valid_events[0]

# --- 2. CSS TASARIM (NEON YEŞİL / DARK MODE) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    :root {
        --bg-main: #0E0E11;
        --card-bg: #151518;
        --card-border: #222226;
        --accent: #00FF85; /* Neon Yeşil */
        --accent-hover: #00cc6a;
        --text-main: #FFFFFF;
        --text-muted: #9CA3AF;
    }

    .stApp { background-color: var(--bg-main); font-family: 'Inter', sans-serif; color: var(--text-main); }
    header { visibility: hidden; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

    /* --- HEADER & LOGO --- */
    .header-logo {
        width: 42px; height: 42px;
        background: linear-gradient(135deg, #00FF85 0%, #0094FF 100%);
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-weight: 800; color: white; font-size: 14px;
        box-shadow: 0 0 15px rgba(0, 255, 133, 0.3);
    }
    .header-title { font-size: 22px; font-weight: 700; color: white; letter-spacing: -0.5px; }

    /* --- ARAMA KUTUSU --- */
    .stTextInput { width: 100%; }
    .stTextInput > div > div > input {
        background-color: #1F1F23 !important;
        color: #EAEAEA !important;
        border: 1px solid #333 !important;
        border-radius: 99px !important;
        padding: 12px 20px !important;
        font-size: 14px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 1px var(--accent) !important;
    }

    /* --- SOL MENÜ BUTONLARI --- */
    div.stButton > button {
        width: 100%;
        background-color: var(--card-bg);
        border: 1px solid var(--card-border);
        color: var(--text-main);
        border-radius: 12px;
        text-align: left;
        padding: 14px 18px;
        font-weight: 500;
        margin-bottom: 6px;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        border-color: var(--accent);
        color: var(--accent);
        transform: translateX(2px);
    }
    /* Aktif buton stili Python tarafında inline CSS ile veriliyor */

    /* --- ORTA KART TASARIMI --- */
    .main-card {
        background-color: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    /* Resim Kutusu */
    .image-frame {
        width: 100%;
        height: 320px; /* Sabit yükseklik */
        background-color: #000; /* Resim sığmazsa arkası siyah kalsın */
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }
    .floating-badge {
        position: absolute; top: 20px; left: 20px;
        background: rgba(0,0,0,0.6); 
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255,255,255,0.1);
        color: white;
        padding: 6px 14px; border-radius: 99px;
        font-size: 12px; font-weight: 600;
        z-index: 5;
    }

    /* Karar Hapı */
    .decision-pill {
        display: inline-flex; align-items: center; gap: 8px;
        padding: 10px 24px; border-radius: 99px;
        font-weight: 800; font-size: 14px; text-transform: uppercase;
        margin-top: -24px; margin-left: 24px; 
        position: relative; z-index: 10;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }

    .content-pad { padding: 24px; padding-top: 12px; }
    
    .section-h { font-size: 18px; font-weight: 700; margin-bottom: 8px; color: white; }
    .desc-p { font-size: 14px; line-height: 1.6; color: var(--text-muted); margin-bottom: 24px; }

    /* Progress Bar */
    .prog-track { background: #2A2A2F; height: 6px; border-radius: 99px; width: 100%; margin-top: 12px; }
    .prog-fill { height: 100%; background: var(--accent); border-radius: 99px; box-shadow: 0 0 10px rgba(0, 255, 133, 0.3); }
    
    /* Analiz Kutusu */
    .note-box {
        background-color: #1A1A1D;
        border: 1px solid #2A2A2F;
        border-radius: 12px;
        padding: 16px;
        margin-top: 24px;
    }

    /* --- SAĞ YORUMCU KARTLARI --- */
    .commentator-card {
        background-color: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 10px;
        display: flex; gap: 12px; align-items: flex-start;
        transition: transform 0.2s;
    }
    .commentator-card:hover { border-color: #333; transform: translateY(-2px); }
    
    .avatar { width: 40px; height: 40px; border-radius: 50%; object-fit: cover; background: #222; }
    
    .icon-circle { 
        width: 24px; height: 24px; border-radius: 50%; 
        display: flex; align-items: center; justify-content: center; 
        font-size: 12px; margin-left: auto; flex-shrink: 0;
    }
    .icon-yes { background: var(--accent); color: black; }
    .icon-no { background: #E53E3E; color: white; }

</style>
""", unsafe_allow_html=True)

# --- 3. ÜST BAR (HEADER) ---
c1, c2 = st.columns([1, 1]) 
with c1:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:20px;">
        <div class="header-logo">VM</div>
        <div class="header-title">VAR Masası</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    # Sadece Arama Kutusu (Sağa Yaslı)
    col_space, col_search = st.columns([1, 2])
    with col_search:
        search_query = st.text_input("ara", placeholder="Pozisyon ara (örn: Gol, Penaltı)...", label_visibility="collapsed")

# --- 4. ANA GRID YAPISI ---
col_left, col_center, col_right = st.columns([3, 6, 3])

# ================= SOL KOLON: LİSTE =================
with col_left:
    st.markdown('<div style="font-weight:700; margin-bottom:15px; color:#fff; font-size:14px; opacity:0.8;">≡ POZİSYON LİSTESİ</div>', unsafe_allow_html=True)
    
    if not df.empty:
        all_events = df['Olay'].dropna().unique()
        
        # Arama Filtresi
        if search_query:
            events_to_show = [e for e in all_events if search_query.lower() in str(e).lower()]
        else:
            events_to_show = all_events

        if len(events_to_show) == 0:
            st.markdown(f"<div style='color:#666; font-size:13px;'>Sonuç bulunamadı.</div>", unsafe_allow_html=True)

        for event in events_to_show:
            is_active = (event == st.session_state.selected_pos_name)
            
            if is_active:
                # Aktif buton için özel stil (Yeşil Kenarlık ve Parlama)
                st.markdown(f"""<style>
                    div.stButton > button[data-testid="baseButton-secondary"] {{
                        border-color: #222;
                    }}
                    div.stButton > button:focus {{
                        background-color: #1A1A1F !important;
                        color: #00FF85 !important;
                        border-color: #00FF85 !important;
                        box-shadow: 0 0 10px rgba(0,255,133,0.1);
                    }}
                </style>""", unsafe_allow_html=True)
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
        
        # Veri Çekme
        ref_decision = safe_get(filtered_df, 'Hakem Karar')
        ref_note = safe_get(filtered_df, 'Yorum')
        match_name = safe_get(filtered_df, 'Maç Adı', 'Bilinmiyor')
        
        # Görsel
        custom_image = safe_get(filtered_df, 'Görsel', '-')
        if custom_image != '-' and custom_image.startswith('http'):
            main_image_url = custom_image
        else:
            main_image_url = "https://images.unsplash.com/photo-1522778119026-d647f0565c6a?auto=format&fit=crop&w=800&q=80"

        # Rozet Ayarları
        decision_text = str(ref_decision).upper()
        badge_style = "background-color: #333; color: white;"
        icon = "⚖️"
        
        if "penaltı" in decision_text.lower(): 
            badge_style = "background-color: #00FF85; color: black;"
            icon = "✅"
        elif "iptal" in decision_text.lower() or "kırmızı" in decision_text.lower():
            badge_style = "background-color: #E53E3E; color: white;"
            icon = "🛑"
        elif "devam" in decision_text.lower():
            badge_style = "background-color: #00FF85; color: black;"
            icon = "▶️"

        # İstatistik
        agree_count = filtered_df[filtered_df['6. sütun'] == 'Evet'].shape[0]
        total = len(filtered_df)
        percent = round((agree_count/total)*100) if total > 0 else 0

        # --- HTML KART (KESİNTİSİZ YAPILANDIRMA) ---
        html_code = f"""
<div class="main-card">
    <div class="image-frame">
        <img src="{main_image_url}" style="width: 100%; height: 100%; object-fit: contain; display: block;">
        <div class="floating-badge">Var İncelemesi</div>
    </div>

    <div style="{badge_style}" class="decision-pill">
        {icon} {decision_text}
    </div>

    <div class="content-pad">
        <div class="section-h">Hakem Kararı</div>
        <div class="desc-p">
            Ceza sahası içerisinde <b>{match_name}</b> maçında yaşanan bu pozisyonda hakem kararı <b>{ref_decision}</b> yönünde olmuştur.
        </div>
        
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
            <span style="font-weight:700; font-size:14px; color:#fff;">Kamuoyu Görüşü</span>
            <span style="color:#00FF85; font-weight:700;">{percent}%</span>
        </div>
        <div class="prog-track">
            <div class="prog-fill" style="width: {percent}%;"></div>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:12px; color:#666; margin-top:6px;">
            <span>Katılıyor</span>
            <span>Katılmıyor</span>
        </div>
        
        <div class="note-box">
            <div style="color:#00FF85; font-weight:600; font-size:13px; margin-bottom:6px;">📄 Analiz Notu</div>
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
    st.markdown('<div style="font-weight:700; margin-bottom:15px; color:#fff; font-size:14px; opacity:0.8;">💬 YORUMCU GÖRÜŞLERİ</div>', unsafe_allow_html=True)
    
    if st.session_state.selected_pos_name and not df.empty:
        for index, row in filtered_df.iterrows():
            y_isim = safe_get(pd.DataFrame([row]), 'Yorumcu', 'Anonim')
            y_yorum = safe_get(pd.DataFrame([row]), 'Yorum', '-')
            y_fikir = safe_get(pd.DataFrame([row]), '6. sütun', 'Hayır')
            
            if y_fikir == 'Evet':
                icon_class = "icon-yes"; icon_symbol = "✔"
            else:
                icon_class = "icon-no"; icon_symbol = "✖"
            
            avatar_url = f"https://i.pravatar.cc/100?u={index+99}"

            commentator_html = f"""
<div class="commentator-card">
    <img src="{avatar_url}" class="avatar">
    <div style="flex:1;">
        <div style="font-weight:600; font-size:14px; margin-bottom:4px; color:#fff;">{y_isim}</div>
        <div style="font-size:12px; color:#9CA3AF; line-height:1.3;">"{y_yorum[:90]}..."</div>
    </div>
    <div class="icon-circle {icon_class}">{icon_symbol}</div>
</div>
"""
            st.markdown(commentator_html, unsafe_allow_html=True)
