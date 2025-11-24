import streamlit as st
import pandas as pd

# --- 1. AYARLAR VE DATA ---
st.set_page_config(page_title="VAR Masası", layout="wide", page_icon="⚽")

G_SHEET_URL = 'https://docs.google.com/spreadsheets/d/10IDYPgr-8C_xmrWtRrTiG3uXiOYLachV3XjhpGlY1Ug/export?format=csv&gid=82638230'

# Session State: Hangi pozisyonun seçili olduğunu hafızada tutmak için
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

# Veri varsa ve henüz seçim yapılmadıysa ilkini seç
if not df.empty and st.session_state.selected_pos_name is None:
    valid_events = df['Olay'].dropna().unique().tolist()
    if valid_events:
        st.session_state.selected_pos_name = valid_events[0]

# --- 2. CSS TASARIM (Readdy Stili) ---
st.markdown("""
<style>
    /* --- GENEL AYARLAR --- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    :root {
        --bg-dark: #0E0E11;
        --card-dark: #1A1A1F;
        --accent-green: #00FF85;
        --accent-purple: #6A0CFF;
        --accent-red: #E53E3E;
        --text-white: #EAEAEA;
        --text-muted: #A0A0A0;
    }

    .stApp {
        background-color: var(--bg-dark);
        font-family: 'Inter', sans-serif;
        color: var(--text-white);
    }
    
    /* Header Gizleme */
    header {visibility: hidden;}
    .block-container { padding-top: 1rem; padding-bottom: 2rem; }

    /* --- BİLEŞEN STİLLERİ --- */
    
    /* KARTLAR (Sol, Orta, Sağ Konteynerler) */
    .custom-card {
        background-color: var(--card-dark);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        height: 100%; /* Kolon yüksekliğini doldur */
    }
    .card-title { font-weight: 700; font-size: 1.1rem; margin-bottom: 15px; display: flex; align-items: center; gap: 8px;}

    /* SOL LİSTE BUTONLARI (Streamlit Butonlarını Özelleştirme) */
    div.stButton > button {
        width: 100%;
        background-color: var(--card-dark);
        border: 1px solid #2A2A2F;
        color: var(--text-white);
        border-radius: 999px; /* Tam yuvarlak */
        text-align: left;
        padding: 12px 20px;
        margin-bottom: 8px;
        font-weight: 600;
        display: flex; justify-content: space-between; align-items: center;
        transition: all 0.2s;
    }
    div.stButton > button:hover { border-color: var(--accent-green); }
    
    /* Aktif Buton Stili (Python tarafında kontrol edilecek) */
    .active-button {
        background-color: var(--accent-green) !important;
        color: black !important;
        border: none !important;
    }
    /* Diğer etiketler */
    .badge-purple { background: #2A1A3F; color: var(--accent-purple); padding: 4px 12px; border-radius: 999px; font-size: 0.75rem; font-weight: 700;}
    .badge-gray { background: #2A2A2F; color: var(--text-muted); padding: 4px 12px; border-radius: 999px; font-size: 0.75rem; font-weight: 700;}


    /* ORTA ALAN - KARAR ETİKETİ */
    .decision-badge {
        display: inline-flex; align-items: center; gap: 8px;
        padding: 8px 20px; border-radius: 999px; font-weight: 700;
        text-transform: uppercase; margin-bottom: 20px; font-size: 0.9rem;
    }
    .badge-green-fill { background: var(--accent-green); color: black; }
    .badge-red-fill { background: var(--accent-red); color: white; }
    .badge-dark-fill { background: #2A2A2F; color: var(--text-white); }

    /* PROGRESS BAR */
    .progress-container {
        background: #2A2A2F; border-radius: 999px; height: 10px; width: 100%; overflow: hidden; margin-top: 10px;
    }
    .progress-fill { height: 100%; background: var(--accent-green); border-radius: 999px; }
    .progress-labels { display: flex; justify-content: space-between; font-size: 0.8rem; color: var(--text-muted); margin-top: 5px; }

    /* ANALİZ NOTU KUTUSU */
    .note-box {
        background: #222227; border-radius: 12px; padding: 15px; margin-top: 20px;
    }
    .note-header { font-weight: 600; margin-bottom: 10px; display: flex; align-items: center; gap: 8px; color: var(--accent-green);}

    /* SAĞ ALAN - YORUMCU KARTLARI */
    .commentator-item {
        display: flex; gap: 12px; padding: 15px;
        background: #222227; border-radius: 12px; margin-bottom: 10px; align-items: flex-start;
    }
    .avatar {
        width: 45px; height: 45px; border-radius: 50%; object-fit: cover;
    }
    .icon-box {
        width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 14px;
    }
    .icon-check { background: var(--accent-green); color: black; }
    .icon-cross { background: var(--accent-red); color: white; }

    /* ÜST BAR (ARAMA & BUTON) */
    .top-bar-input {
        background: var(--card-dark); border: 1px solid #2A2A2F; color: var(--text-muted);
        padding: 8px 15px; border-radius: 999px; outline: none; width: 250px;
    }
    .top-bar-btn {
        background: var(--accent-green); color: black; padding: 8px 20px; border-radius: 999px;
        font-weight: 600; border: none; cursor: pointer;
    }

</style>
""", unsafe_allow_html=True)

# --- 3. ÜST BAR (HEADER) ---
c1, c2 = st.columns([1, 2])
with c1:
    st.markdown('<div style="display: flex; align-items: center; gap: 12px; font-size: 1.5rem; font-weight: 700;"><div style="width:40px;height:40px;background:var(--accent-green);border-radius:50%;display:flex;align-items:center;justify-content:center;color:black;font-weight:bold;">VC</div>VAR Masası</div>', unsafe_allow_html=True)
with c2:
    # Sağ tarafa arama ve buton (Görsel amaçlı HTML)
    st.markdown("""
    <div style="display: flex; justify-content: flex-end; gap: 15px; align-items: center;">
        <input type="text" class="top-bar-input" placeholder="Pozisyon ara...">
        <button class="top-bar-btn">Yeni Analiz Ekle</button>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True) # Boşluk

# --- 4. ANA IZGARA (GRID) ---
col_left, col_center, col_right = st.columns([3, 6, 3])

# --- SOL KOLON: POZİSYON LİSTESİ ---
with col_left:
    st.markdown("""
    <div class="custom-card">
        <div class="card-title"><span style="color:var(--accent-green);">≡</span> Pozisyon Listesi</div>
    """, unsafe_allow_html=True)
    
    if not df.empty:
        unique_events = df['Olay'].dropna().unique()
        
        for event in unique_events:
            is_active = (event == st.session_state.selected_pos_name)
            
            # Aktif buton için özel stil uygula
            if is_active:
                 st.markdown(f"""
                 <style>
                 div.stButton > button[data-testid="baseButton-secondary"][aria-label="{event}"] {{
                     background-color: var(--accent-green) !important;
                     color: black !important;
                     border: none !important;
                 }}
                 div.stButton > button[data-testid="baseButton-secondary"][aria-label="{event}"]::after {{
                     content: "Aktif"; margin-left: auto; font-size: 0.8rem;
                 }}
                 </style>
                 """, unsafe_allow_html=True)

            # --- DÜZELTME BURADA ---
            # label=event kısmını sildim, sadece 'event' yeterli.
            if st.button(event, key=f"btn_{event}", use_container_width=True):
                st.session_state.selected_pos_name = event
                st.rerun()
                
    st.markdown("</div>", unsafe_allow_html=True)

# --- ORTA KOLON: DETAY ---
with col_center:
    if st.session_state.selected_pos_name and not df.empty:
        selected_pos = st.session_state.selected_pos_name
        filtered_df = df[df['Olay'] == selected_pos]
        
        # Verileri çek
        ref_decision = safe_get(filtered_df, 'Hakem Karar')
        ref_note = safe_get(filtered_df, 'Yorum')
        match_name = safe_get(filtered_df, 'Maç Adı', 'Bilinmiyor')
        dakika = "23. Dakika" # Veride dakika yoksa placeholder

        # Badge rengi
        badge_cls = "badge-dark-fill"
        badge_icon = "⚖️"
        if "penaltı" in str(ref_decision).lower(): badge_cls = "badge-green-fill"; badge_icon="✅"
        elif "kırmızı" in str(ref_decision).lower(): badge_cls = "badge-red-fill"; badge_icon="🟥"
        elif "devam" in str(ref_decision).lower() or "doğru" in str(ref_decision).lower(): badge_cls = "badge-green-fill"; badge_icon="✅"

        # İstatistik
        agree_count = filtered_df[filtered_df['6. sütun'] == 'Evet'].shape[0]
        total = len(filtered_df)
        percent = round((agree_count/total)*100) if total > 0 else 0

        st.markdown(f"""
        <div class="custom-card" style="padding:0; overflow:hidden;">
            <div style="height: 300px; position: relative; background: url('https://images.unsplash.com/photo-1522778119026-d647f0565c6a?auto=format&fit=crop&w=800&q=80') center/cover;">
                <div style="position: absolute; top: 15px; left: 15px; background: #6A0CFF; color: white; padding: 5px 15px; border-radius: 999px; font-weight: 700; font-size: 0.8rem;">{dakika}</div>
            </div>
            
            <div style="padding: 25px;">
                <div class="decision-badge {badge_cls}">
                    <span>{badge_icon}</span> {str(ref_decision).upper()}
                </div>
                
                <h2 style="margin-bottom: 15px;">Hakem Kararı</h2>
                <p style="color: var(--text-white); line-height: 1.6; opacity: 0.9;">
                    {match_name} maçında yaşanan bu pozisyonda hakem kararı <b>{ref_decision}</b> yönünde olmuştur.
                </p>
                
                <div style="margin-top: 30px; margin-bottom: 30px;">
                    <div style="display: flex; justify-content: space-between; font-weight: 700; margin-bottom: 5px;">
                        <span>Kamuoyu Görüşü</span>
                        <span style="color:var(--accent-green);">{percent}%</span>
                    </div>
                    <div class="progress-container">
                        <div class="progress-fill" style="width: {percent}%;"></div>
                    </div>
                    <div class="progress-labels">
                        <span>Katılıyor</span>
                        <span>Katılmıyor</span>
                    </div>
                </div>
                
                <div class="note-box">
                    <div class="note-header">📄 Analiz Notu</div>
                    <p style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.5;">
                        {ref_note}
                    </p>
                </div>

            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Lütfen soldaki listeden bir pozisyon seçiniz.")

# --- SAĞ KOLON: YORUMCULAR ---
with col_right:
    st.markdown("""
    <div class="custom-card">
        <div class="card-title">💬 Yorumcu Görüşleri</div>
    """, unsafe_allow_html=True)
    
    if st.session_state.selected_pos_name and not df.empty:
        for index, row in filtered_df.iterrows():
            y_isim = safe_get(pd.DataFrame([row]), 'Yorumcu', 'Anonim')
            y_yorum = safe_get(pd.DataFrame([row]), 'Yorum', '-')
            y_fikir = safe_get(pd.DataFrame([row]), '6. sütun', 'Hayır')
            
            is_agree = (y_fikir == 'Evet')
            icon_cls = "icon-check" if is_agree else "icon-cross"
            icon_symbol = "✔" if is_agree else "✖"
            
            # Avatar için rastgele bir resim (Gerçek veride URL olmalı)
            avatar_url = f"https://i.pravatar.cc/100?u={index}"

            st.markdown(f"""
            <div class="commentator-item">
                <img src="{avatar_url}" class="avatar">
                <div style="flex: 1;">
                    <div style="font-weight: 700; margin-bottom: 4px;">{y_isim}</div>
                    <div style="color: var(--text-muted); font-size: 0.85rem; line-height: 1.4;">
                        "{y_yorum[:120]}..."
                    </div>
                </div>
                <div class="icon-box {icon_cls}">{icon_symbol}</div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)
