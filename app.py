import streamlit as st
import pandas as pd

# --- 1. AYARLAR VE DATA ---
st.set_page_config(page_title="Var Masası", layout="wide", page_icon="⚽")

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
    # Boş olmayan ilk olayı bul
    valid_events = df['Olay'].dropna().unique().tolist()
    if valid_events:
        st.session_state.selected_pos_name = valid_events[0]

# --- 2. CSS TASARIM ---
st.markdown("""
<style>
    /* Global Reset & Dark Theme */
    .stApp {
        background-color: #0E0E11;
        font-family: 'Inter', sans-serif;
        color: #EAEAEA;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Header Gizleme */
    header {visibility: hidden;}
    
    /* BUTON STİLLERİ (Sol Liste İçin) */
    div.stButton > button {
        width: 100%;
        background-color: #0B0B0D;
        border: 1px solid #222228;
        color: #EAEAEA;
        border-radius: 8px;
        text-align: left;
        padding: 10px 15px;
        transition: all 0.2s;
        display: flex;
        justify-content: flex-start;
    }
    
    div.stButton > button:hover {
        border-color: #0094FF;
        color: #0094FF;
        background-color: #121217;
    }

    div.stButton > button:focus {
        border-color: #0094FF;
        background-color: #0094FF;
        color: white;
    }
    
    /* Kart Stilleri */
    .glass-card {
        background: rgba(17,17,19,0.55);
        backdrop-filter: blur(6px);
        border: 1px solid #222228;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    .inner-card {
        background: #0B0B0D;
        border: 1px solid #1A1A1F;
        border-radius: 12px;
        padding: 16px;
    }

    /* Badge & Text */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
    }
    .badge-blue { background: #0094FF; color: white; }
    .badge-dark { background: #121217; color: #EAEAEA; border: 1px solid #222228; }
    .badge-red { background: #E53E3E; color: white; }
    .badge-green { background: #38A169; color: white; }
    .muted { color: rgba(234,234,234,0.65); font-size: 0.85rem; }

    /* Yorumcu Listesi */
    .commentator-item {
        display: flex; gap: 12px; padding: 12px;
        background: #0B0B0D; border: 1px solid #1A1A1F;
        border-radius: 12px; margin-bottom: 10px;
    }
    .avatar {
        width: 40px; height: 40px; border-radius: 50%;
        background: #1A1A1F; display: flex; align-items: center; 
        justify-content: center; font-weight: bold; color: #0094FF;
    }
    
    /* Progress Bar */
    .progress-bg { background:#121217; border-radius:999px; height:8px; width:100%; margin-top:8px; overflow:hidden;}
    .progress-fill { height:100%; background: linear-gradient(90deg,#0094FF,#6a0cff); }

</style>
""", unsafe_allow_html=True)

# --- 3. ÜST BAR ---
col_h1, col_h2 = st.columns([1, 2])
with col_h1:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
        <div style="width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #0094FF, #FFC700); display: flex; align-items: center; justify-content: center; font-weight: bold; color: #000;">VC</div>
        <h2 style="font-size: 1.5rem; color: white;">Var Masası</h2>
    </div>
    """, unsafe_allow_html=True)

# --- 4. ANA IZGARA ---
col_left, col_center, col_right = st.columns([3, 6, 3])

# --- SOL KOLON: TIKLANABİLİR LİSTE ---
with col_left:
    st.markdown("""
    <div class="glass-card" style="padding-bottom: 10px;">
        <h3 style="font-size: 1rem; margin-bottom: 15px;">Pozisyon Listesi</h3>
        <div style="opacity: 0.7; font-size: 0.85rem; margin-bottom: 10px;">Son eklenen olaylar:</div>
    </div>
    """, unsafe_allow_html=True)
    
    if not df.empty:
        # Benzersiz olayları al
        unique_events = df['Olay'].dropna().unique()
        
        # Her olay için bir Streamlit butonu oluştur
        for event in unique_events:
            # Butona basılırsa session_state'i güncelle
            if st.button(event, key=f"btn_{event}", use_container_width=True):
                st.session_state.selected_pos_name = event
                st.rerun() # Sayfayı yenile ki orta kısım güncellensin

# --- ORTA KOLON: DETAY (BUG FİX YAPILDI) ---
with col_center:
    # Seçili pozisyon varsa işle
    if st.session_state.selected_pos_name and not df.empty:
        selected_pos = st.session_state.selected_pos_name
        filtered_df = df[df['Olay'] == selected_pos]
        
        # Verileri çek
        ref_decision = safe_get(filtered_df, 'Hakem Karar')
        ref_note = safe_get(filtered_df, 'Yorum')
        match_name = safe_get(filtered_df, 'Maç Adı', 'Bilinmiyor')
        
        # Badge rengi
        badge_cls = "badge-dark"
        if "penaltı" in str(ref_decision).lower(): badge_cls = "badge-blue"
        elif "kırmızı" in str(ref_decision).lower(): badge_cls = "badge-red"
        elif "devam" in str(ref_decision).lower() or "doğru" in str(ref_decision).lower(): badge_cls = "badge-green"

        # İstatistik
        agree_count = filtered_df[filtered_df['6. sütun'] == 'Evet'].shape[0]
        total = len(filtered_df)
        percent = round((agree_count/total)*100) if total > 0 else 0

        # HTML KART OLUŞTURMA (String birleştirme hatası düzeltildi)
        html_card = f"""
        <div class="glass-card">
            <div style="margin-bottom: 15px;">
                <span class="badge badge-dark">{match_name}</span>
                <span class="badge badge-blue" style="margin-left: 5px;">VAR İncelemesi</span>
            </div>
            
            <div style="background: #0B0B0D; border: 1px solid #1A1A1F; border-radius: 12px; height: 300px; display: flex; align-items: center; justify-content: center; overflow: hidden; margin-bottom: 20px;">
                <img src="https://images.unsplash.com/photo-1522778119026-d647f0565c6a?auto=format&fit=crop&w=800&q=80" style="width: 100%; height: 100%; object-fit: cover; opacity: 0.8;">
            </div>
            
            <div class="inner-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div>
                        <div style="font-size: 1.1rem; font-weight: 600;">Hakem Kararı: {ref_decision}</div>
                    </div>
                    <div class="badge {badge_cls}">{str(ref_decision).upper()}</div>
                </div>
                <div class="muted" style="margin-top: 10px; line-height: 1.5;">
                    <span style="color: #0094FF; font-weight:bold;">Analiz Notu:</span> {ref_note}
                </div>
            </div>
            
            <div style="margin-top: 20px; padding: 12px; border: 1px solid #222228; border-radius: 12px;">
                <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 5px;">
                    <span class="muted">Hakemle aynı görüşteki yorumcular</span>
                    <span style="font-weight: bold;">%{percent}</span>
                </div>
                <div class="progress-bg">
                    <div class="progress-fill" style="width: {percent}%;"></div>
                </div>
            </div>
        </div>
        """
        st.markdown(html_card, unsafe_allow_html=True)
    else:
        st.info("Lütfen soldaki listeden bir pozisyon seçiniz.")

# --- SAĞ KOLON: YORUMCULAR ---
with col_right:
    st.markdown("""
    <div class="glass-card">
        <h3 style="font-size: 1rem; margin-bottom: 15px;">Yorumcular</h3>
    """, unsafe_allow_html=True)
    
    if st.session_state.selected_pos_name and not df.empty:
        for index, row in filtered_df.iterrows():
            y_isim = safe_get(pd.DataFrame([row]), 'Yorumcu', 'Anonim')
            y_yorum = safe_get(pd.DataFrame([row]), 'Yorum', '-')
            y_fikir = safe_get(pd.DataFrame([row]), '6. sütun', 'Hayır')
            
            icon = "✅" if y_fikir == 'Evet' else "❌"
            initial = y_isim[0] if len(y_isim) > 0 else "A"
            
            st.markdown(f"""
            <div class="commentator-item">
                <div class="avatar">{initial}</div>
                <div style="flex: 1;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                        <span style="font-weight: 600; font-size: 0.9rem;">{y_isim}</span>
                        <span style="font-size: 0.8rem;">{icon}</span>
                    </div>
                    <div class="muted" style="font-size: 0.8rem; line-height: 1.4;">
                        "{y_yorum[:100]}..."
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)
