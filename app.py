import time
import subprocess

# --- KURULUM ---
print("⚙️ Tasarım yenileniyor... (30-40 sn sürebilir)")
!pip install streamlit -q
!wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared
!chmod +x cloudflared

# --- UYGULAMA DOSYASI (TASARIMLI) ---
with open("app.py", "w") as f:
    f.write("""
import streamlit as st
import pandas as pd

# 1. Sayfa Ayarları (Geniş Mod)
st.set_page_config(page_title="VAR Masası", page_icon="⚽", layout="wide")

# 2. CSS İLE TASARIM (MAKYAJ KISMI)
st.markdown(\"""
    <style>
    /* Ana Arka Plan Rengi */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Yan Menü Rengi */
    [data-testid="stSidebar"] {
        background-color: #262730;
    }
    
    /* Kartların Tasarımı */
    .pozisyon-karti {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        border-left: 6px solid #4CAF50; /* Yeşil Çizgi */
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    .karti-kirmizi {
        border-left: 6px solid #FF5252 !important; /* Kırmızı Çizgi */
    }
    
    /* Başlıklar */
    h1, h2, h3 {
        font-family: 'Sans-Serif';
        color: #ffffff;
    }
    
    /* Metinler */
    p {
        color: #e0e0e0;
        font-size: 16px;
    }
    </style>
\""", unsafe_allow_html=True)

# --- BAŞLIK ALANI ---
col_logo, col_text = st.columns([1, 5])
with col_logo:
    st.write("⚽") # Buraya ileride logo da koyabiliriz
with col_text:
    st.title("VAR MASASI")
    st.markdown("*Türkiye'nin En Ateşli Tartışma Platformu*")

# --- VERİ SAKLAMA ---
if 'pozisyonlar' not in st.session_state:
    # Örnek veri ile başlatalım ki boş görünmesin
    st.session_state.pozisyonlar = [
        {"Maç": "FB - TS", "Olay": "Osayi'nin ceza sahasında düşürülmesi", "Hakem": "Ali Şansalan", "Resmi Karar": "Penaltı", "Yorumcu": "Ahmet Çakar", "Durum": "❌ Katılmıyor", "Yorum": "Kendini yere atıyor, hakem eyyam yaptı."}
    ]

# --- YAN MENÜ (VERİ GİRİŞİ) ---
with st.sidebar:
    st.header("📝 Yeni Kayıt Gir")
    mac_adi = st.text_input("Maç Adı", placeholder="Örn: GS - BJK")
    olay = st.text_area("Olay/Pozisyon", placeholder="Pozisyonu kısaca anlat...")
    hakem_adi = st.text_input("Hakem", placeholder="Hakem Adı")
    resmi_karar = st.selectbox("Sahadaki Karar", ["Penaltı", "Devam", "Gol", "Ofsayt", "Kırmızı Kart"])
    
    st.markdown("---")
    st.subheader("📺 Yorumcu Görüşü")
    yorumcu_adi = st.selectbox("Yorumcu", ["Ahmet Çakar", "Erman Toroğlu", "Rıdvan Dilmen", "Trio", "Fırat Aydınus"])
    yorumcu_karar = st.radio("Yorumcu Katılıyor mu?", ["✅ Katılıyor", "❌ Katılmıyor"])
    yorum_metni = st.text_input("Yorum Özeti", placeholder="Ne dedi?")
    
    if st.button("Listeye Ekle", type="primary"):
        if mac_adi and olay:
            st.session_state.pozisyonlar.insert(0, { # En üste ekle
                "Maç": mac_adi, "Olay": olay, "Hakem": hakem_adi,
                "Resmi Karar": resmi_karar, "Yorumcu": yorumcu_adi,
                "Durum": yorumcu_karar, "Yorum": yorum_metni
            })
            st.success("Pozisyon eklendi!")

# --- ANA EKRAN (KART GÖRÜNÜMÜ) ---
st.subheader(f"🔥 Güncel Gündem ({len(st.session_state.pozisyonlar)} Pozisyon)")

# İstatistikler (Üstte şık durur)
c1, c2, c3 = st.columns(3)
df = pd.DataFrame(st.session_state.pozisyonlar)
c1.metric("Toplam Tartışma", len(df))
c2.metric("Hakemi Destekleyen", len(df[df["Durum"] == "✅ Katılıyor"]))
c3.metric("Hakeme Karşı Çıkan", len(df[df["Durum"] == "❌ Katılmıyor"]))

st.markdown("---")

# Döngü ile her pozisyonu KART olarak basıyoruz
for p in st.session_state.pozisyonlar:
    # Rengi belirle (Katılıyorsa yeşil, katılmıyorsa kırmızı kenarlık)
    renk_class = "pozisyon-karti"
    if p["Durum"] == "❌ Katılmıyor":
        renk_class += " karti-kirmizi"
        
    # HTML Kodu (Kart Tasarımı)
    html_code = f\"""
    <div class="{renk_class}">
        <h3 style="margin:0; color:#fff;">{p['Maç']} <span style="font-size:14px; color:#aaa;">(Hakem: {p['Hakem']})</span></h3>
        <p style="margin-top:5px; color:#ccc;"><i>"{p['Olay']}"</i></p>
        <div style="background-color:rgba(255,255,255,0.1); padding:10px; border-radius:5px; margin-top:10px;">
            <strong style="color:#FFD700;">{p['Yorumcu']} Diyor ki:</strong><br>
            <span style="font-size:18px;">{p['Durum']}</span> - {p['Yorum']}
        </div>
        <p style="font-size:12px; margin-top:5px; text-align:right;">Resmi Karar: <b>{p['Resmi Karar']}</b></p>
    </div>
    \"""
    st.markdown(html_code, unsafe_allow_html=True)

""")

# --- UYGULAMAYI BAŞLAT ---
print("🚀 Tasarım yüklendi, site açılıyor...")
subprocess.Popen(["streamlit", "run", "app.py"])
time.sleep(3)

print("\n👇 AŞAĞIDAKİ LİNKE TIKLA (Şifre Yok!):")
!./cloudflared tunnel --url http://localhost:8501
