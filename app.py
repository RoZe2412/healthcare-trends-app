# --- Imports ---
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import requests
import time

# --- Page Config ---
st.set_page_config(
    page_title="Healthcare Global Trends AI",
    page_icon="🌍",
    layout="wide",
)

# --- Session State ---
if 'entered' not in st.session_state:
    st.session_state.entered = False
if 'page' not in st.session_state:
    st.session_state.page = 'Home'
if 'theme' not in st.session_state:
    st.session_state.theme = 'Light'

# --- Theme Settings ---
def get_theme_colors():
    if st.session_state.theme == "Light":
        return {
            'bg_color': '#ffffff',
            'text_color': '#1a1a1a',
            'hover_color': '#3399ff',
            'container_color': '#f5f5f5',
            'chart_template': 'plotly_white'
        }
    else:
        return {
            'bg_color': '#121212',
            'text_color': '#eeeeee',
            'hover_color': '#0077b6',
            'container_color': '#1e1e1e',
            'chart_template': 'plotly_dark'
        }

colors = get_theme_colors()

# --- Custom CSS Styling ---
st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(to bottom right, {colors['bg_color']}, {colors['hover_color']});
}}

h1, h2, h3, h4, h5, h6, p, .stMetricValue {{
    color: {colors['text_color']};
}}

.container {{
    background-color: {colors['container_color']};
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
}}

.topnav {{
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-bottom: 30px;
}}

/* ALL buttons: nav, enter, form, etc. */
button, .stButton > button {{
    background-color: white !important;
    color: white !important;
    font-weight: bold;
    font-size: 16px;
    padding: 10px 20px;
    border-radius: 8px !important;
    border: 2px solid #ccc !important;
}}

/* Hover style for all buttons */
button:hover, .stButton > button:hover {{
    background-color: #eeeeee !important;
    color: black !important;
    border-color: #999 !important;
    transition: 0.3s;
}}
</style>
""", unsafe_allow_html=True)

# --- Landing Page ---
if not st.session_state.entered:
    st.markdown("""
    <div style="height: 90vh; display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <img src="https://cdn-icons-png.flaticon.com/512/3774/3774299.png" width="120"/>
        <h1>🌍</h1>
        <p>Using AI and Data to Transform Global Health.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 ENTER SITE"):
        st.session_state.entered = True
    st.stop()

# --- Theme Toggle ---
col1, col2 = st.columns([10, 1])
with col2:
    if st.button("🌙 / ☀️"):
        st.session_state.theme = 'Dark' if st.session_state.theme == 'Light' else 'Light'
        st.experimental_rerun()
colors = get_theme_colors()

# --- Navigation Bar ---
st.markdown('<div class="topnav">', unsafe_allow_html=True)
cols = st.columns(8)
pages = ["Home", "Dashboard", "Trends", "Travel", "Education", "Alerts", "About", "Chatbot"]
for i, page_name in enumerate(pages):
    with cols[i]:
        if st.button(page_name):
            st.session_state.page = page_name
st.markdown('</div>', unsafe_allow_html=True)

# --- Pages ---
if st.session_state.page == 'Home':
    st.header("🏠 Home")
    st.markdown(f"""
    <div class="container" style="text-align: center;">
        <h1>Empowering Global Healthcare 🌍</h1>
        <p>Live Monitoring | AI-Driven Insights | Smart Health Alerts</p>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == 'Dashboard':
    st.header("📊 Dashboard")
    disease = st.selectbox("Select Disease:", ["COVID-19", "Flu (Simulated)", "Monkeypox (Simulated)", "Dengue Fever (Simulated)"])
    with st.spinner("Loading data..."):
        if disease == "COVID-19":
            try:
                data = requests.get("https://disease.sh/v3/covid-19/countries").json()
                df = pd.DataFrame(data)
                df['lat'] = df['countryInfo'].apply(lambda x: x['lat'])
                df['long'] = df['countryInfo'].apply(lambda x: x['long'])
            except:
                st.error("Failed to load data.")
        else:
            df = pd.DataFrame({
                "country": ["USA", "India", "Brazil", "France"],
                "cases": np.random.randint(2000, 9000, 4),
                "lat": [37.1, 20.5, -14.2, 46.2],
                "long": [-95.7, 78.9, -51.9, 2.2]
            })
        fig = px.scatter_geo(df, lat="lat", lon="long", size="cases",
                             hover_name="country", color="cases",
                             projection="natural earth",
                             template=colors['chart_template'])
        st.plotly_chart(fig, use_container_width=True)

elif st.session_state.page == 'Trends':
    st.header("📈 Trends")
    disease = st.selectbox("Choose a disease:", ["COVID-19", "Flu", "Monkeypox", "Dengue"])
    dates = pd.date_range(end=pd.Timestamp.today(), periods=30)
    if disease == "COVID-19":
        try:
            data = requests.get("https://disease.sh/v3/covid-19/historical/all?lastdays=30").json()
            df = pd.DataFrame({
                "date": list(data["cases"].keys()),
                "cases": list(data["cases"].values())
            })
            df["date"] = pd.to_datetime(df["date"])
        except:
            df = pd.DataFrame({"date": dates, "cases": np.random.randint(1000, 5000, 30)})
    else:
        df = pd.DataFrame({"date": dates, "cases": np.random.randint(1000, 5000, 30)})
    fig = px.line(df, x="date", y="cases", title=f"{disease} Trends (30 Days)", template=colors['chart_template'])
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.page == 'Travel':
    st.header("🛫 Travel Advisories")
    st.markdown("""
    - Dengue outbreak in Southeast Asia  
    - COVID-19 precautions in Europe  
    - Monkeypox alerts in France, USA
    """)

elif st.session_state.page == 'Education':
    st.header("📚 Education Center")
    st.markdown("""
    - **COVID-19**: Respiratory virus.  
    - **Flu**: Viral seasonal illness.  
    - **Monkeypox**: Rash and fever.  
    - **Dengue**: Mosquito-borne illness.
    """)

elif st.session_state.page == 'Alerts':
    st.header("🔔 Subscribe to Health Alerts")
    email = st.text_input("Enter your email:")
    if st.button("Subscribe"):
        if email:
            st.success(f"{email} subscribed successfully!")
        else:
            st.warning("Please enter a valid email.")

elif st.session_state.page == 'About':
    st.header("ℹ️ About This Project")
    st.markdown("""
    - **Team**: Varshaan & Meetika  
    - **Goal**: Track global disease trends  
    - **Tech**: Streamlit, Plotly, Python  
    - **Chatbot**: health assistant  
    - **GitHub**: github.com/varshaanp/healthcare-trends-app
    """)

elif st.session_state.page == 'Chatbot':
    st.header("Healthcare Chatbot")
    user_question = st.text_input("Ask your health question:")

    def get_reply(q):
        q = q.lower()
        if "covid" in q:
            return "COVID-19 is a respiratory virus. Stay up to date on boosters."
        elif "flu" in q:
            return "Flu is seasonal. Annual vaccines help prevent it."
        elif "dengue" in q:
            return "Dengue is mosquito-borne. Use repellent and avoid bites."
        elif "monkeypox" in q:
            return "Monkeypox causes rash and fever. Avoid close contact."
        elif "symptom" in q:
            return "Symptoms vary. Fever, cough, fatigue are common."
        else:
            return "Try asking about COVID-19, flu, dengue, or symptoms."

    if st.button("Get Response"):
        if user_question.strip():
            st.success(get_reply(user_question))
        else:
            st.info("Please enter a question.")
