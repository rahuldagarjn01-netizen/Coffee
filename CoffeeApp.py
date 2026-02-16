import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# --- 1. CONFIGURATION & BRANDING ---
st.set_page_config(page_title="Candour Coffee | Executive Dashboard", layout="wide")

# Custom CSS for a "Premium Craft" look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { 
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 12px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #eee;
    }
    h1, h2, h3 { color: #3d2b1f; }
    </style>
    """, unsafe_allow_html=True)


# --- 2. OPERATIONAL DATA MODELS (Direct from Report) ---
# Inventory Model 
ROP_VAL = 37              # Reorder Point (kg)
EOQ_VAL = 215             # Economic Order Quantity (kg)
SAFETY_STOCK = 12.5       # Safety Buffer (kg)

# Capacity Model [cite: 125, 194]
BASELINE_CT = 35.0        # Manual Process
OPTIMIZED_CT = 29.0       # U-Shaped Layout
AUTOMATED_CT = 12.0       # Semi-Automation Goal
SHIFT_SEC = 7 * 3600      # 7-hour effective shift [cite: 183]

# --- 3. HELPER FUNCTIONS ---
def get_kpi_color(value, red, yellow):
    """Implementation of Traffic Light System """
    if value >= red: return "🔴 CRITICAL", "error"
    if value >= yellow: return "🟡 WARNING", "warning"
    return "🟢 OPTIMAL", "success"

import base64

def main():
# --- BACKGROUND IMAGE LOGIC ---
    def get_base64(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()

    try:
        # This looks for your Background.jpeg file
        bin_str = get_base64('Background.jpeg')
        st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
    }}
    
    /* FIX: This makes Titles, Headers, AND the 'Focus' line bold and glowing */
    h1, h2, h3, p, span, b, strong {{
        color: #3d2b1f !important;
        text-shadow: 2px 2px 8px rgba(255, 255, 255, 1), 
                     -2px -2px 8px rgba(255, 255, 255, 1);
        font-weight: 800 !important;
    }}

    /* Keeps your data cards clear and solid */
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.9); /* Increased opacity to 90% */
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }}
    
    </style>
    """, unsafe_allow_html=True)
    except Exception as e:
        st.error("Background image not found. Ensure 'Background.jpeg' is in the folder.")

    # --- SIDEBAR: LOGO & INPUTS ---
    try:
        st.sidebar.image("logo.png", use_container_width=True)
    except:
        st.sidebar.title("☕ Candour Coffee")
    
    st.sidebar.markdown("---")
    st.sidebar.header("🕹️ Live Operations Input")
    st.sidebar.info("Update these values based on real-time floor data to bridge the 'Visibility Gap.")
    
    curr_stock = st.sidebar.number_input("Current Stock (kg)", value=45)
    curr_cycle = st.sidebar.slider("Current Cycle Time (sec)", 10, 50, 29)
    curr_defect = st.sidebar.slider("Defect Rate (%)", 0.0, 5.0, 1.2)

    # --- HEADER ---
    st.title("🚀 Operational Nervous System: Vikhroli Facility")

    st.markdown("""
        <style>
        /* This forces the container box to be SOLID WHITE */
        [data-testid="stNotification"] {
            background-color: #FFFFFF !important;
            opacity: 1 !important;
            border: 2px solid #3d2b1f !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3) !important;
        }

        /* This removes the 'transy' green/red background inside the box */
        [data-testid="stNotification"] > div {
            background-color: transparent !important;
            opacity: 1 !important;
        }

        /* This makes your text (Inventory Level: Healthy) Pitch Black and Extra Bold */
        [data-testid="stNotification"] p {
            color: #000000 !important;
            font-weight: 900 !important;
            opacity: 1 !important;
        }
        </style>
        """, unsafe_allow_html=True)
    st.markdown(f"**Focus: Efficiency & Excellence*")
    
    # st.image("roastery.jpg", caption="Candour Coffee Roastery Operations", use_container_width=True)
    
    st.markdown("---")

    # --- SECTION 1: INVENTORY INTELLIGENCE ---
    st.header("1. Inventory Strategy & Liquidity")
    i_col1, i_col2, i_col3 = st.columns(3)
    
    with i_col1:
        st.metric("Warehouse Stock", f"{curr_stock} kg")
        if curr_stock <= ROP_VAL:
            st.error(f"🚨 ALERT: Stock hit ROP ({ROP_VAL}kg). Order {EOQ_VAL}kg immediately!")
        else:
            st.success("Inventory Level: Healthy")

    with i_col2:
        st.metric("Optimal Order (EOQ)", f"{EOQ_VAL} kg")
        st.caption("Calculated to minimize holding vs. ordering costs.")

    with i_col3:
        st.metric("Safety Stock", f"{SAFETY_STOCK} kg")
        st.caption("5-day buffer for Mumbai logistics.")

    # --- SECTION 2: PRODUCTION KPIs (Traffic Lights) ---
    st.markdown("---")
    st.header("2. Real-Time Production Visibility")
    p_col1, p_col2, p_col3 = st.columns(3)

    with p_col1:
        status, level = get_kpi_color(curr_cycle, 40, 35)
        st.metric("Cycle Time", f"{curr_cycle}s", delta=f"{curr_cycle - BASELINE_CT}s")
        getattr(st, level)(f"Status: {status}")

    with p_col2:
        status, level = get_kpi_color(curr_defect, 3.0, 2.0)
        st.metric("Defect Rate", f"{curr_defect}%")
        getattr(st, level)(f"Status: {status}")

    with p_col3:
        hourly_output = int(3600 / curr_cycle)
        st.metric("Hourly Throughput", f"{hourly_output} Units")
        st.caption("Current productivity ceiling.")

    # --- SECTION 3: TREND ANALYSIS (Fatigue Detection) ---
    st.markdown("---")
    st.header("3. Productivity Trend Analysis")
    
    # Data simulating the afternoon fatigue mentioned in the report
    trend_data = pd.DataFrame({
        'Hour': ['9AM', '10AM', '11AM', '12PM', '2PM', '3PM', '4PM'],
        'Cycle Time (s)': [30, 29, 29, 31, 35, 38, curr_cycle]
    })
    
    fig_trend = px.line(trend_data, x='Hour', y='Cycle Time (s)', 
                        title="Shift Cycle Time: Detecting Worker Fatigue", 
                        markers=True, color_discrete_sequence=['#3d2b1f'])
    fig_trend.add_hline(y=40, line_dash="dash", line_color="red", annotation_text="Critical Limit")
    st.plotly_chart(fig_trend, use_container_width=True)

    # --- SECTION 4: SCALABILITY SIMULATOR ---
    st.markdown("---")
    st.header("4. Scalability & Investment Simulation")
    
    sim_data = pd.DataFrame({
        'Stage': ['Manual (Baseline)', 'U-Layout (Optimized)', 'Semi-Automation'],
        'Daily Capacity': [SHIFT_SEC/BASELINE_CT, SHIFT_SEC/OPTIMIZED_CT, SHIFT_SEC/AUTOMATED_CT]
    })
    
    fig_cap = px.bar(sim_data, x='Stage', y='Daily Capacity', color='Stage', 
                     text_auto='.0f', title="Capacity Growth Modeling (Units per 7-Hr Shift)")
    st.plotly_chart(fig_cap, use_container_width=True)
    
    st.info("💡 **Recommendation:** Trigger Level 2 Automation when daily demand exceeds 600 units.")
    
# --- SECTION 5: FACILITY VISUALS ---
    st.markdown("---")
    st.header("5. Vikhroli Facility Gallery")
    
    st.markdown("""
        <style>
        [data-testid="stImage"] img {
            height: 300px;
            object-fit: cover;
            border-radius: 10px;
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <style>
        [data-testid="stSidebar"] [data-testid="stImage"] img {
            height: auto !important; 
            width: 100% !important;
            object-fit: contain !important; 
            border-radius: 0px !important; 
        }
        </style>
        """, unsafe_allow_html=True)
    
    # You can display images in columns or a single large view
    pic_col1, pic_col2, pic_col3, pic_col4, pic_col5, pic_col6, pic_col7, pic_col8 = st.columns(8)
    
    with pic_col1:
        st.image("1.jpeg", use_container_width=True)
    
    with pic_col2:
        st.image("2.jpeg", use_container_width=True)

    with pic_col3:
        st.image("3.jpeg", use_container_width=True)

    with pic_col4:
        st.image("4.jpeg", use_container_width=True)
    
    with pic_col5:
        st.image("5.jpeg", use_container_width=True)

    with pic_col6:
        st.image("6.jpeg", use_container_width=True)

    with pic_col7:
        st.image("7.jpeg", use_container_width=True)

    with pic_col8:
        st.image("8.jpeg", use_container_width=True)

if __name__ == "__main__":
    main()