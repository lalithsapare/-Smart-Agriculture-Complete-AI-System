import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# ====================== PAGE CONFIG ======================
st.set_page_config(
    layout="wide",
    page_title="Smart Agri AI",
    page_icon="🌾",
    initial_sidebar_state="expanded"
)

# ====================== CUSTOM CSS ======================
st.markdown("""
<style>
    .main-header { font-size: 2.8rem; font-weight: 800; color: #1B5E20; text-align: center; }
    .sub-header { font-size: 1.3rem; color: #388E3C; text-align: center; margin-bottom: 20px; }
    .metric-box { background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%); padding: 15px; border-radius: 12px; border: 2px solid #4CAF50; }
    .success-box { background: #E8F5E9; padding: 15px; border-radius: 10px; border-left: 5px solid #2E7D32; }
    .info-box { background: #E3F2FD; padding: 15px; border-radius: 10px; border-left: 5px solid #1976D2; }
</style>
""", unsafe_allow_html=True)

# ====================== TITLE ======================
st.markdown('<p class="main-header">🌾 Smart Agriculture Complete AI System</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Weather Forecast • Crop Recommendation • Yield Prediction • Fertilizer & Irrigation Optimization</p>', unsafe_allow_html=True)

# ====================== SIDEBAR INPUTS ======================
st.sidebar.header("🌱 Step 1: Enter Farm Details")
area = st.sidebar.slider("🌾 Farm Area (acres)", 1, 50, 10)
N = st.sidebar.slider("🧪 Nitrogen (kg/ha)", 0, 200, 90)
P = st.sidebar.slider("🧪 Phosphorus (kg/ha)", 0, 150, 50)
K = st.sidebar.slider("🧪 Potassium (kg/ha)", 0, 180, 60)

st.sidebar.header("🌡️ Step 2: Weather & Soil")
humidity = st.sidebar.slider("💧 Humidity (%)", 20, 95, 70)
temperature = st.sidebar.slider("🌡️ Current Temp (°C)", 18, 38, 28)
rainfall = st.sidebar.slider("🌧️ Rainfall (mm - last 24h)", 30, 200, 85)
ph = st.sidebar.slider("🪴 Soil pH", 4.5, 8.5, 6.5)

# CSV Upload (Optional)
uploaded_file = st.sidebar.file_uploader("📁 Upload Historical Data (CSV)", type="csv")
history_df = None
if uploaded_file is not None:
    try:
        history_df = pd.read_csv(uploaded_file)
        st.sidebar.success(f"✅ Loaded {len(history_df)} records")
    except Exception as e:
        st.sidebar.error(f"❌ Error: {e}")

# ====================== ANALYSIS BUTTON ======================
if st.button("🚀 RUN COMPLETE AI ANALYSIS", type="primary", use_container_width=True):
    
    with st.spinner("🤖 AI is processing soil, weather, and crop data..."):
        
        # 1. Weather Prediction
        pred_temp = temperature + np.random.normal(0, 1.5)
        pred_rain = max(0, rainfall * (1 + np.random.normal(0, 0.12)))
        
        # 2. Soil Health Score (0-100)
        ph_score = max(0, 100 - abs(ph - 6.5) * 12)
        npk_score = min(100, (N + P + K) / 3)
        moisture_score = min(100, humidity)
        soil_health_score = int((ph_score * 0.3 + npk_score * 0.4 + moisture_score * 0.3))
        
        # 3. Crop Recommendation
        scores = {
            'Rice': N*0.12 + P*0.06 + (100-rainfall)*0.025 + humidity*0.008,
            'Maize': N*0.09 + K*0.13 + temperature*0.035 - (ph-6)*0.05,
            'Wheat': P*0.16 + humidity*0.012 + ph*0.09 + (30-temperature)*0.02,
            'Cotton': K*0.20 + (temperature-25)*0.045 + N*0.03 - (ph-6.5)*0.07,
            'Sugarcane': rainfall*0.025 + N*0.08 + area*0.012 + humidity*0.005,
            'Groundnut': P*0.14 + K*0.11 + (ph-5.5)*0.06 - rainfall*0.01,
            'Red Chili': N*0.07 + K*0.16 + (temperature-26)*0.03 + (ph-6)*0.04
        }
        recommended_crop = max(scores, key=scores.get)
        best_score = scores[recommended_crop]
        
        advice_map = {
            'Rice': "🌾 Kharif crop. Flooded conditions needed. Variety: PRH-10.",
            'Maize': "🌽 Rabi crop. Composite hybrid. Apply 50% N at 30 DAS.",
            'Wheat': "🌾 Winter crop. Variety: HD-2967. Irrigate at crown root.",
            'Cotton': "🌿 Bt Cotton. 4-5 irrigations. Watch for bollworm.",
            'Sugarcane': "🍬 Plant Feb-Mar. Variety: Co-1148. Max water at grand growth.",
            'Groundnut': "🥜 Variety: TGDK-98. No waterlogging. Apply gypsum at flowering.",
            'Red Chili': "🌶️ Variety: Jwala/Teja. Drip irrigation. Spray for thrips."
        }
        crop_advice = advice_map.get(recommended_crop, "Soil test recommended.")
        
        # 4. FIXED Yield Prediction
        base_yields = {'Rice': 35, 'Maize': 28, 'Wheat': 30, 'Cotton': 8, 'Sugarcane': 350, 'Groundnut': 12, 'Red Chili': 6}
        base = base_yields.get(recommended_crop, 20)
        factor = (N/90)*0.25 + (P/50)*0.20 + (K/60)*0.20 + (rainfall/85)*0.15 + (humidity/70)*0.10 + 0.10
        yield_per_acre = base * factor
        yield_est = yield_per_acre * area
        
        # Historical average (safe handling)
        hist_avg = 20.0
        if history_df is not None:
            for col in ['yield', 'Yield', 'YIELD', 'yield_qtls']:
                if col in history_df.columns:
                    hist_avg = history_df[col].mean()
                    break
        
        # 5. Fertilizer & Irrigation
        fert_rec = []
        if N < 60: fert_rec.append("🔴 Urea 60kg/ha")
        elif N < 90: fert_rec.append("🟠 Urea 45kg/ha")
        else: fert_rec.append("🟢 Urea Maintain")
        if P < 30: fert_rec.append("DAP 40kg/ha")
        elif P < 50: fert_rec.append("DAP 20kg/ha")
        if K < 40: fert_rec.append("MOP 30kg/ha")
        elif K < 60: fert_rec.append("MOP 15kg/ha")
        fertilizer = " + ".join(fert_rec) if fert_rec else "Balanced NPK"
        
        if humidity < 45 or temperature > 35:
            irrigation_need = "🔴 High (14-16mm/day) - Drip Mandatory"
        elif humidity < 65 or temperature > 30:
            irrigation_need = "🟠 Medium (8-10mm/day)"
        else:
            irrigation_need = "🟢 Low (4-6mm/day) - Rain Sufficient"

    # ====================== RESULTS DISPLAY ======================
    st.markdown("### 📊 AI Analysis Results")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("🌡️ Predicted Temp", f"{pred_temp:.1f}°C", delta=f"{pred_temp-temperature:+.1f}°C")
    with c2:
        st.metric("🌧️ Predicted Rain", f"{pred_rain:.0f}mm", delta=f"{pred_rain-rainfall:+.0f}mm")
    with c3:
        st.metric("🌱 Best Crop", recommended_crop.upper())
    with c4:
        st.metric("📦 Total Yield", f"{yield_est:.0f} qtls", delta=f"{yield_per_acre:.1f} qtls/acre")
    
    c5, c6, c7 = st.columns(3)
    with c5:
        st.metric("🧪 Fertilizer Plan", fertilizer)
    with c6:
        st.metric("💧 Irrigation Need", irrigation_need)
    with c7:
        st.metric("🩺 Soil Health", f"{soil_health_score}/100", 
                  delta="✅ Excellent" if soil_health_score > 80 else "⚠️ Moderate" if soil_health_score > 60 else "🔴 Poor")
    
    st.success("✅ Analysis Complete! View graphs below.")

    # ====================== GRAPHS SECTION ======================
    st.markdown("### 📈 Visual Analytics & Predictions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌾 Crop Suitability Scores")
        crop_df = pd.DataFrame(list(scores.items()), columns=['Crop', 'Score'])
        crop_df = crop_df.sort_values('Score', ascending=True)
        st.bar_chart(crop_df.set_index('Crop'))
    
    with col2:
        st.subheader("🧪 NPK Soil Balance")
        npk_df = pd.DataFrame({
            'Current': [N, P, K],
            'Optimal': [90, 50, 60]
        }, index=['Nitrogen', 'Phosphorus', 'Potassium'])
        st.bar_chart(npk_df, color=['#FF9800', '#4CAF50'])

    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("🌡️🌧️ Weather Prediction (Next 24h)")
        weather_df = pd.DataFrame({
            'Current': [temperature, rainfall],
            'Predicted': [pred_temp, pred_rain]
        }, index=['Temperature (°C)', 'Rainfall (mm)'])
        st.bar_chart(weather_df, color=['#FF9800', '#4CAF50'])
    
    with col4:
        st.subheader("📦 Current vs AI-Predicted Yield (Next 24h)")
        
        # **FINAL FIXED YIELD DATA** - 2 columns = 2 colors
        yield_data = pd.DataFrame({
            'Current/Historical': [hist_avg],
            'AI-Predicted': [yield_per_acre]
        })
        
        st.bar_chart(
            yield_data,
            height=300,
            color=['#FF9800', '#4CAF50']
        )
        
        st.metric("🎯 AI Predicted", f"{yield_per_acre:.1f} qtls/acre", 
                  delta=f"{yield_per_acre-hist_avg:+.1f}")
        st.caption(f"For {recommended_crop} • {area} acres")

    col5, col6 = st.columns(2)
    
    with col5:
        st.markdown("### 🌿 Crop Guidance")
        st.info(f"**{recommended_crop.upper()}**\n\n{crop_advice}")
    
    with col6:
        st.markdown("### 🧪 Action Plan")
        st.success(f"**Fertilizer**: {fertilizer}")
        st.info(f"**Irrigation**: {irrigation_need}")

    # ====================== EXPORT ======================
    st.markdown("### 📥 Download Report")
    report = pd.DataFrame({
        'Parameter': ['Crop', 'Yield (Total)', 'Yield/acre', 'Temp', 'Rain', 'Fertilizer', 'Irrigation', 'Soil Health'],
        'Value': [recommended_crop, f"{yield_est:.0f}", f"{yield_per_acre:.1f}", 
                  f"{pred_temp:.1f}°C", f"{pred_rain:.0f}mm", fertilizer, irrigation_need, f"{soil_health_score}%"]
    })
    csv = report.to_csv(index=False).encode('utf-8')
    st.download_button("📄 Download CSV", csv, f"agri_report_{recommended_crop}.csv", "text/csv")

# ====================== FOOTER ======================
st.markdown("---")
st.markdown("💡 **Smart Farming AI for AP/Telangana Farmers** | 🌾 v2.0")