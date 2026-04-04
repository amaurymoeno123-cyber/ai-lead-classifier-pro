import streamlit as st
import os
import json
from dotenv import load_dotenv
from scraper import extract_info
from classifier import classify_lead
from database import save_to_supabase
from streamlit_extras.add_vertical_space import add_vertical_space
from utils import update_env_file

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Lead Classifier | AmauryDev",
    page_icon="⚡",
    layout="wide",
)

# Load environment variables
load_dotenv()

# --- Custom Styling ---
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("styles.css")

# --- Session State for Keys ---
if "groq_key" not in st.session_state:
    st.session_state.groq_key = os.getenv("GROQ_API_KEY", "")
if "supabase_url" not in st.session_state:
    st.session_state.supabase_url = os.getenv("SUPABASE_URL", "")
if "supabase_key" not in st.session_state:
    st.session_state.supabase_key = os.getenv("SUPABASE_KEY", "")

# --- Sidebar Management ---
with st.sidebar:
    st.markdown("<h1 style='color: #8a2be2; text-align: center; margin-bottom: 0;'>⚡ AmauryDev</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; opacity: 0.6; font-size: 0.9rem;'>AI Intelligence Platform</p>", unsafe_allow_html=True)
    st.divider()
    
    st.subheader("⚙️ Configuración")
    # Groq Settings
    g_k = st.text_input("Groq API Key", value=st.session_state.groq_key, type="password", help="Obtenla en console.groq.com")
    if g_k != st.session_state.groq_key:
        st.session_state.groq_key = g_k
        
    # Supabase Settings
    s_u = st.text_input("Supabase URL", value=st.session_state.supabase_url)
    if s_u != st.session_state.supabase_url:
        st.session_state.supabase_url = s_u
        
    s_k = st.text_input("Supabase Key", value=st.session_state.supabase_key, type="password")
    if s_k != st.session_state.supabase_key:
        st.session_state.supabase_key = s_k
        
    if st.button("💾 Guardar en .env", use_container_width=True):
        try:
            update_env_file("GROQ_API_KEY", st.session_state.groq_key)
            update_env_file("SUPABASE_URL", st.session_state.supabase_url)
            update_env_file("SUPABASE_KEY", st.session_state.supabase_key)
            st.success("Guardado ✅")
        except Exception as e:
            st.error(f"Error: {e}")

    # Readiness
    is_ready = bool(st.session_state.groq_key and st.session_state.supabase_url and st.session_state.supabase_key)
    add_vertical_space(1)
    if is_ready:
        st.success("Status: Ready (Pro) 🟢")
    else:
        st.info("Status: Demo Mode 🟡")

    add_vertical_space(10)
    
    # Branding Section
    st.markdown(f"""
        <div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 15px; font-size: 0.8rem; opacity: 0.8;">
            <p style="margin-bottom: 5px;">Created by <b>Amaury Moreno Vidal</b></p>
            <p style="margin-bottom: 5px;">LinkedIn: <a href="https://www.linkedin.com/in/amaury-moreno-vidal-24132a369/" target="_blank">View Profile</a></p>
            <p>GitHub: <a href="https://github.com/amaurymoreno123-cyber" target="_blank">amaurymoreno123-cyber</a></p>
        </div>
    """, unsafe_allow_html=True)

# --- Analysis Logic ---
def run_analysis(url):
    os.environ["GROQ_API_KEY"] = st.session_state.groq_key
    os.environ["SUPABASE_URL"] = st.session_state.supabase_url
    os.environ["SUPABASE_KEY"] = st.session_state.supabase_key
    
    if not is_ready:
        with st.status("Analyzing Demo Lead...", expanded=False) as status:
            st.write("Extracting data...")
            st.write("Generating mock analysis...")
            status.update(label="Demo Finish!", state="complete")
        return {
            "company_name": "AmauryDev Corp",
            "needs_ai": True,
            "priority_score": 10,
            "technical_reason": "Vuestra web tiene un alto potencial para la implementación de agentes autónomos.",
            "custom_pitch": "Hola! He analizado tu web. Me gustaría enseñarte cómo la IA puede disparar vuestro negocio."
        }

    with st.status("Processing AI Analysis...", expanded=True) as status:
        st.write("1. Reading website content...")
        t = extract_info(url)
        if not t:
            status.update(label="Scraping Failed", state="error")
            return None
            
        st.write("2. AI Classification with Llama 3...")
        c = classify_lead(t)
        if not c:
            status.update(label="AI Brain Failure", state="error")
            return None
            
        st.write("3. Syncing with Supabase Cloud...")
        save_to_supabase(c)
        status.update(label="Analysis Successful", state="complete", expanded=False)
        return c

# --- Dashboard Layout ---
st.markdown("<h1 style='text-align: center; font-size: 3rem;'>AI Lead <span style='color: #8a2be2;'>Classifier</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.7; font-size: 1.1rem;'>The intelligence core behind <b>AmauryDev</b>.</p>", unsafe_allow_html=True)

add_vertical_space(2)

# Central Input
c_i1, c_i2, c_i3 = st.columns([1, 2, 1])
with c_i2:
    target = st.text_input("Enter Company URL:", placeholder="https://example.com", label_visibility="collapsed")
    add_vertical_space(1)
    sub1, sub2, sub3 = st.columns([1, 1, 1])
    with sub2:
        run_btn = st.button("RUN ANALYSIS 🚀", use_container_width=True)

if run_btn:
    if not target.startswith("http"):
        st.error("Please enter a valid URL.")
    else:
        ans = run_analysis(target)
        if ans:
            st.divider()
            
            # Key Results
            c_m1, c_m2, c_m3 = st.columns(3)
            with c_m1:
                st.container(border=True).metric("Empresa", ans['company_name'])
            with c_m2:
                p = ans['priority_score']
                st.container(border=True).metric("Prioridad", f"{p}/10")
            with c_m3:
                f = "IA" if ans['needs_ai'] else "Desarrollo Web"
                st.container(border=True).metric("Foco Principal", f)
            
            add_vertical_space(1)
            
            # Content Columns
            cl1, cl2 = st.columns([2, 1])
            with cl1:
                with st.container(border=True):
                    st.subheader("💡 Razón para el servicio")
                    st.write(ans['technical_reason'])
            
            with cl2:
                with st.container(border=True):
                    # Priority Color Indicator
                    p = ans['priority_score']
                    if p >= 8:
                        st.success("🔥 LEAD CALIENTE")
                    elif p >= 5:
                        st.warning("⚖️ TIBIO")
                    else:
                        st.error("❄️ FRIO")

            add_vertical_space(1)
            
            # Pitch Area
            with st.container(border=True):
                st.subheader("📢 Sales Pitch Personalizado")
                st.markdown(f"""
                    <div style="background-color: rgba(138, 43, 226, 0.1); padding: 20px; border-radius: 8px; font-style: italic;">
                        "{ans['custom_pitch']}"
                    </div>
                """, unsafe_allow_html=True)
                add_vertical_space(1)
                st.caption("Copia este mensaje para tu contacto inicial.")

else:
    add_vertical_space(5)
    st.markdown("<div style='text-align: center; opacity: 0.3;'>Ready to process. Waiting for URL...</div>", unsafe_allow_html=True)

# Footer Branding
st.divider()
st.markdown(f"""
    <div style="text-align: center; opacity: 0.5; padding: 20px;">
        AI Lead Classifier | Developed by <b>Amaury Moreno Vidal</b> | <a href="https://github.com/amaurymoreno123-cyber" target="_blank">amaurymoreno123-cyber</a>
    </div>
""", unsafe_allow_html=True)
