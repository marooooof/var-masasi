# --- ORTA: DETAY ---
with col_center:
    if st.session_state.selected_pos_name and not df.empty:
        selected_pos = st.session_state.selected_pos_name
        filtered_df = df[df['Olay'] == selected_pos]
        
        # Verileri çek
        ref_decision = safe_get(filtered_df, 'Hakem Karar')
        ref_note = safe_get(filtered_df, 'Yorum')
        match_name = safe_get(filtered_df, 'Maç Adı', 'Bilinmiyor')
        
        # --- YENİ KISIM: GÖRSEL SEÇİMİ ---
        # E-Tabloda 'Görsel' sütununu ara, yoksa varsayılanı kullan
        custom_image = safe_get(filtered_df, 'Görsel', '-')
        
        # Eğer tabloda link varsa onu kullan, yoksa varsayılan stadyum resmini kullan
        if custom_image != '-' and custom_image.startswith('http'):
            main_image_url = custom_image
        else:
            main_image_url = "https://images.unsplash.com/photo-1522778119026-d647f0565c6a?auto=format&fit=crop&w=800&q=80"
        # ---------------------------------

        dakika = "Var İncelemesi"

        badge_cls = "badge-dark-fill"
        badge_icon = "⚖️"
        decision_text = str(ref_decision).upper() if ref_decision != '-' else "KARAR BELİRSİZ"
        
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
    <div style="height: 300px; position: relative; background: url('{main_image_url}') center/cover;">
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
        st.info("Soldaki arama çubuğunu kullanarak bir pozisyon seçin.")
