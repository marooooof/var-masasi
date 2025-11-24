import streamlit as st
import pandas as pd

# --- 1. AYARLAR VE DATA ---
st.set_page_config(page_title="VAR Masası", layout="wide", page_icon="⚽")

G_SHEET_URL = 'https://docs.google.com/spreadsheets/d/10IDYPgr-8C_xmrWtRrTiG3uXiOYLachV3XjhpGlY1Ug/export?format=csv&gid=82638230'

# Session State
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

# Otomatik ilk seçimi yap
if not df.empty and st.session_state.selected_pos_name is None:
    valid_events = df['Olay'].dropna().unique().tolist()
    if valid_events:
        st.session_state.selected_pos_name = valid_events[0]

# --- 2. CSS TASARIM ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    :root {
        --bg-dark: #0E0E11;
        --card-dark: #1A1A1F;
        --accent-green: #00FF85;
        --accent-purple: #6A0CFF;
        --accent-red: #E53E3E;
        --text-white: #EAEAEA;
        --text-muted: #A0A0A0;
        --search-bg: #27272A;
    }

    .stApp { background-color: var(--bg-dark); font-family: 'Inter', sans-serif; color: var(--text-white); }
    header { visibility: hidden; }
    .block-container { padding-top: 1rem; padding-bottom: 2rem; }

    /* --- ÖZEL ARAMA KUTUSU STİLİ (Streamlit Input Override) --- */
    /* Input kutusunun kendisi */
    .stTextInput > div > div > input {
        background-color: var(--search-bg) !important;
        color: #EAEAEA !important;
        border: 1px solid #3F3F46 !important;
        border-radius: 99px !important; /* Hap Şekli */
        padding: 10px 20px !important;
        font-size: 0.9rem !important;
    }
    /* Input odaklanınca */
    .stTextInput > div > div > input:focus {
        border-color: var(--accent-green) !important;
        box-shadow: 0 0 0 1px var(--accent-green) !important;
    }
    /* SVG arama ikonu gizleme (opsiyonel temizlik) */
    .stTextInput svg { display: none; }

    /* Kartlar */
    .custom-card {
        background-color: var(--card-dark);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #2A2A2F;
    }
    .card-title { font-weight: 700; font-size: 1.1rem; margin-bottom: 15px; display: flex; align-items: center; gap: 8px; color: var(--accent-green);}

    /* SOL LİSTE BUTONLARI */
    div.stButton > button {
        width: 100%;
        background-color: var(--card-dark);
        border: 1px solid #2A2A2F;
        color: var(--text-white);
        border-radius: 999px;
        text-align: left;
        padding: 12px 20px;
        font-weight: 600;
        margin-bottom: 5px;
    }
    div.stButton > button:hover { border-color: var(--accent-green); color: var(--accent-green); }
    div.stButton > button:focus { background-color: var(--accent-green) !important; color: black !important; border-color: var(--accent-green) !important; }

    /* DİĞER ETİKETLER */
    .decision-badge {
        display: inline-flex; align-items: center; gap: 8px;
        padding: 8px 20px; border-radius: 999px; font-weight: 700;
        text-transform: uppercase; margin-bottom: 20px; font-size: 0.9rem;
    }
    .badge-green-fill { background: var(--accent-green); color: black; }
    .badge-red-fill { background: var(--accent-red); color: white; }
    .badge-dark-fill { background: #2A2A2F; color: var(--text-white); }

    .progress-container { background: #2A2A2F; border-radius: 999px; height: 10px; width: 100%; overflow: hidden; margin-top: 10px; }
    .progress-fill { height: 100%; background: var(--accent-green); border-radius: 999px; }
    .progress-labels { display: flex; justify-content: space-between; font-size: 0.8rem; color: var(--text-muted); margin-top: 5px; }

    .note-box { background: #222227; border-radius: 12px; padding: 15px; margin-top: 20px; border: 1px solid #2A2A2F;}
    .note-header { font-weight: 600; margin-bottom: 5px; color: var(--accent-green); display: flex; align-items: center; gap: 6px;}

    .commentator-item {
        display: flex; gap: 12px; padding: 15px;
        background: #222227; border-radius: 12px; margin-bottom: 10px; align-items: flex-start; border: 1px solid #2A2A2F;
    }
    .avatar { width: 45px; height: 45px; border-radius: 50%; object-fit: cover; background: #333;}
    .icon-box { width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 14px; }
    .icon-check { background: var(--accent-green); color: black; }
    .icon-cross { background: var(--accent-red); color: white; }
    
    .top-bar-btn { background: var(--accent-green); color: black; padding: 8px 20px; border-radius: 999px; font-weight: 600; border: none; cursor: pointer; height: 42px;}

</style>
""", unsafe_allow_html=True)

# --- 3. HEADER (ÇALIŞAN ARAMA KUTUSU İLE) ---
c1, c2 = st.columns([1, 2])
with c1:
    st.markdown('<div style="display: flex; align-items: center; gap: 12px; font-size: 1.5rem; font-weight: 700; margin-bottom: 20px;"><div style="width:40px;height:40px;background:var(--accent-green);border-radius:50%;display:flex;align-items:center;justify-content:center;color:black;font-weight:bold;">VC</div>VAR Masası</div>', unsafe_allow_html=True)

with c2:
    # Burayı 2 sütuna bölüyoruz: Arama Kutusu | Buton
    search_col, btn_col = st.columns([3, 1])
    
    with search_col:
        # İŞTE BURASI: HTML DEĞİL, GERÇEK STREAMLIT INPUT
        # label_visibility="collapsed" diyerek üstündeki etiketi gizliyoruz, sadece kutu kalıyor.
        search_query = st.text_input("Ara", placeholder="Pozisyon ara...", label_visibility="collapsed")
    
    with btn_col:
        # Buton sadece görsel şu an
        st.markdown('<button class="top-bar-btn" style="width:100%">Yeni Analiz Ekle</button>', unsafe_allow_html=True)

# --- 4. GRID ---
col_left, col_center, col_right = st.columns([3, 6, 3])

# --- SOL: FİLTRELENMİŞ LİSTE ---
with col_left:
    st.markdown('<div class="custom-card"><div class="card-title">≡ Pozisyon Listesi</div>', unsafe_allow_html=True)
    
    if not df.empty:
        all_events = df['Olay'].dropna().unique()
        
        # PYTHON FİLTRELEME MANTIĞI BURADA
        if search_query:
            # Arama kutusuna bir şey yazıldıysa listeyi filtrele
            filtered_events = [e for e in all_events if search_query.lower() in str(e).lower()]
        else:
            # Boşsa hepsini göster
            filtered_events = all_events

        if len(filtered_events) == 0:
             st.markdown(f"<div style='color:#A0A0A0; font-size:0.9rem;'>'{search_query}' bulunamadı.</div>", unsafe_allow_html=True)

        for event in filtered_events:
            # Butona basılırsa seçimi güncelle
            if st.button(event, key=f"btn_{event}", use_container_width=True):
                st.session_state.selected_pos_name = event
                st.rerun()
                
    st.markdown("</div>", unsafe_allow_html=True)

# --- ORTA: DETAY ---
with col_center:
    if st.session_state.selected_pos_name and not df.empty:
        selected_pos = st.session_state.selected_pos_name
        filtered_df = df[df['Olay'] == selected_pos]
        
        ref_decision = safe_get(filtered_df, 'Hakem Karar')
        ref_note = safe_get(filtered_df, 'Yorum')
        match_name = safe_get(filtered_df, 'Maç Adı', 'Bilinmiyor')
        dakika = "Var İncelemesi"

        badge_cls = "badge-dark-fill"
        badge_icon = "⚖️"
        decision_text = str(ref_decision).upper()
        
        if "penaltı" in str(ref_decision).lower(): 
            badge_cls = "badge-green-fill"
            badge_icon = "✅"
        elif "kırmızı" in str(ref_decision).lower(): 
            badge_cls = "badge-red-fill"
            badge_icon = "🟥"
        elif "devam" in str(ref_decision).lower(): 
            badge_cls = "badge-green-fill"
            badge_icon = "▶️"

        agree_count = filtered_df[filtered_df['6. sütun'] == 'Evet'].shape[0]
        total = len(filtered_df)
        percent = round((agree_count/total)*100) if total > 0 else 0

        html_content = f"""
<div class="custom-card" style="padding:0; overflow:hidden; border: none;">
    <div style="height: 300px; position: relative; background: url('https://images.unsplash.com/photo-1522778119026-d647f0565c6a?auto=format&fit=crop&w=800&q=80') center/cover;">
        <div style="position: absolute; top: 15px; left: 15px; background: #6A0CFF; color: white; padding: 5px 15px; border-radius: 999px; font-weight: 700; font-size: 0.8rem;">{dakika}</div>
    </div>
    <div style="padding: 25px; background-color: var(--card-dark); border: 1px solid #2A2A2F; border-top: none; border-bottom-left-radius: 16px; border-bottom-right-radius: 16px;">
        <div class="decision-badge {badge_cls}">
            <span>{badge_icon}</span> {decision_text}
        </div>
        <h2 style="margin-bottom: 10px; color: white;">Hakem Kararı</h2>
        <p style="color: var(--text-white); line-height: 1.6; opacity: 0.9; margin-bottom: 20px;">
            <b>{match_name}</b> maçında yaşanan bu pozisyonda hakem kararı <b>{ref_decision}</b> yönünde olmuştur.
        </p>
        <div style="margin-bottom: 25px;">
            <div style="display: flex; justify-content: space-between; font-weight: 700; margin-bottom: 5px;">
                <span style="color:var(--text-white)">Kamuoyu Görüşü</span>
                <span style="color:var(--accent-green);">{percent}%</span>
            </div>
            <div class="progress-container">
                <div class="progress-fill" style="width: {percent}%;"></div>
            </div>
            <div class="progress-labels" style="display:flex; justify-content:space-between; font-size:0.8rem; color:#A0A0A0; margin-top:5px;">
                <span>Katılıyor</span>
                <span>Katılmıyor</span>
            </div>
        </div>
        <div class="note-box">
            <div class="note-header">📄 Analiz Notu</div>
            <p style="color: #A0A0A0; font-size: 0.9rem; line-height: 1.5; margin:0;">
                {ref_note}
            </p>
        </div>
    </div>
</div>
"""
        st.markdown(html_content, unsafe_allow_html=True)
        
    else:
        st.info("Soldan bir pozisyon seçin.")

# --- SAĞ: YORUMCULAR ---
with col_right:
    st.markdown('<div class="custom-card"><div class="card-title">💬 Yorumcu Görüşleri</div>', unsafe_allow_html=True)
    
    if st.session_state.selected_pos_name and not df.empty:
        for index, row in filtered_df.iterrows():
            y_isim = safe_get(pd.DataFrame([row]), 'Yorumcu', 'Anonim')
            y_yorum = safe_get(pd.DataFrame([row]), 'Yorum', '-')
            y_fikir = safe_get(pd.DataFrame([row]), '6. sütun', 'Hayır')
            
            is_agree = (y_fikir == 'Evet')
            icon_cls = "icon-check" if is_agree else "icon-cross"
            icon_symbol = "✔" if is_agree else "✖"
            initial = y_isim[0] if len(y_isim) > 0 else "A"

            commentator_html = f"""
<div class="commentator-item">
    <div class="avatar">{initial}</div>
    <div style="flex: 1;">
        <div style="font-weight: 700; margin-bottom: 4px; color: var(--text-white);">{y_isim}</div>
        <div style="color: #A0A0A0; font-size: 0.85rem; line-height: 1.4;">
            "{y_yorum[:100]}..."
        </div>
    </div>
    <div class="icon-box {icon_cls}">{icon_symbol}</div>
</div>
"""
            st.markdown(commentator_html, unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)
