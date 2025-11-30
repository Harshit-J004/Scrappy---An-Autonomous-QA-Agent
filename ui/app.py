import streamlit as st
import requests
import json
import os

# Configuration
import streamlit as st
import requests
import json
import os

# Configuration
API_URL = "http://localhost:8000"

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="QA // AGENT",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# NIKE-INSPIRED 'VOID' CSS SYSTEM
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Teko:wght@300;400;600;700&display=swap');

    /* ---------------------------------------------------------------------
       RESET & CORE
       --------------------------------------------------------------------- */
    :root {
        --bg-color: #000000;
        --card-bg: #090909;
        --text-primary: #FFFFFF;
        --text-secondary: #666666;
        --accent: #D0F20F; /* VOLT */
        --border: #222222;
    }

    .stApp {
        background-color: var(--bg-color);
        color: var(--text-primary);
    }

    /* ---------------------------------------------------------------------
       TYPOGRAPHY
       --------------------------------------------------------------------- */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Teko', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    h1 {
        font-size: 6rem !important;
        font-weight: 600 !important;
        line-height: 0.9 !important;
        margin-bottom: 0.5rem !important;
        color: var(--text-primary) !important;
    }

    h2 {
        font-size: 2.5rem !important;
        font-weight: 400 !important;
        color: var(--text-primary) !important;
        border-left: 3px solid var(--accent);
        padding-left: 15px;
        margin-top: 3rem !important;
        margin-bottom: 1.5rem !important;
    }

    h3 {
        font-size: 1.5rem !important;
        font-weight: 400 !important;
        color: var(--text-secondary) !important;
        margin-bottom: 1rem !important;
    }

    p, label, li, .stMarkdown {
        font-family: 'Inter', sans-serif !important;
        font-weight: 300;
        color: #CCCCCC !important;
        font-size: 1rem;
        line-height: 1.6;
    }

    /* ---------------------------------------------------------------------
       SIDEBAR
       --------------------------------------------------------------------- */
    [data-testid="stSidebar"] {
        background-color: #050505;
        border-right: 1px solid var(--border);
    }
    
    [data-testid="stSidebar"] .block-container {
        padding-top: 3rem;
    }

    /* ---------------------------------------------------------------------
       COMPONENTS: BUTTONS
       --------------------------------------------------------------------- */
    .stButton > button {
        background-color: transparent;
        color: var(--text-primary) !important;
        border: 1px solid var(--text-primary);
        border-radius: 0;
        padding: 15px 40px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.9rem;
        letter-spacing: 2px;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        width: 100%;
    }

    .stButton > button:hover {
        background-color: var(--accent);
        color: #000000 !important;
        border-color: var(--accent);
        transform: translateY(-2px);
    }

    .stButton > button:active {
        transform: scale(0.98);
    }

    /* ---------------------------------------------------------------------
       COMPONENTS: INPUTS
       --------------------------------------------------------------------- */
    .stTextInput > div > div > input {
        background-color: transparent;
        color: var(--text-primary);
        border: none;
        border-bottom: 1px solid var(--border);
        border-radius: 0;
        padding: 15px 0;
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
    }

    .stTextInput > div > div > input:focus {
        border-bottom-color: var(--accent);
        box-shadow: none;
    }

    /* ---------------------------------------------------------------------
       COMPONENTS: FILE UPLOADER
       --------------------------------------------------------------------- */
    [data-testid="stFileUploader"] {
        background-color: var(--card-bg);
        border: 1px dashed var(--border);
        border-radius: 0;
        padding: 2rem;
        transition: all 0.3s ease;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: var(--accent);
        background-color: #0f0f0f;
    }

    /* ---------------------------------------------------------------------
       COMPONENTS: CARDS & EXPANDERS
       --------------------------------------------------------------------- */
    .streamlit-expanderHeader {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border);
        border-radius: 0 !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif;
        text-transform: uppercase;
        font-size: 0.9rem;
        letter-spacing: 1px;
    }
    
    .streamlit-expanderContent {
        background-color: transparent;
        border: 1px solid var(--border);
        border-top: none;
        color: var(--text-secondary);
    }

    /* ---------------------------------------------------------------------
       UTILITIES
       --------------------------------------------------------------------- */
    .badge {
        display: inline-block;
        padding: 4px 8px;
        background: var(--border);
        color: var(--text-secondary);
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1rem;
    }

    .stat-box {
        border: 1px solid var(--border);
        padding: 20px;
        text-align: center;
    }
    
    .stat-value {
        font-family: 'Teko', sans-serif;
        font-size: 3rem;
        color: var(--accent);
        line-height: 1;
    }
    
    .stat-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* HIDE STREAMLIT BRANDING */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* RADIO BUTTONS CUSTOM */
    .stRadio > label {
        font-family: 'Teko', sans-serif !important;
        font-size: 1.5rem !important;
        color: var(--text-secondary) !important;
        transition: color 0.3s;
    }
    .stRadio > label:hover {
        color: var(--text-primary) !important;
    }

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style='margin-bottom: 3rem;'>
            <div style='font-family: "Teko"; font-size: 2rem; font-weight: 700; color: #FFF; letter-spacing: 2px;'>
                QA // AGENT
            </div>
            <div style='font-family: "Inter"; font-size: 0.7rem; color: #666; letter-spacing: 1px;'>
                AUTONOMOUS TESTING SUITE
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    page = st.radio(
        "NAVIGATION",
        ["01 / KNOWLEDGE", "02 / SCENARIOS", "03 / EXECUTION"],
        label_visibility="collapsed"
    )
    
    st.markdown("""
        <div style='position: fixed; bottom: 2rem; left: 2rem; right: 2rem;'>
            <div style='border-top: 1px solid #222; padding-top: 1rem;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <span style='color: #444; font-size: 0.7rem;'>ENGINE</span>
                    <span style='color: #D0F20F; font-size: 0.7rem; font-weight: bold;'>GEMINI 2.0</span>
                </div>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-top: 0.5rem;'>
                    <span style='color: #444; font-size: 0.7rem;'>STATUS</span>
                    <span style='color: #FFF; font-size: 0.7rem;'>ONLINE</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MAIN LAYOUT
# -----------------------------------------------------------------------------

# HERO SECTION
st.markdown("""
    <div style='margin-bottom: 4rem;'>
        <span class='badge'>VERSION 3.0</span>
        <h1>AUTONOMOUS<br><span style='color: #333;'>INTELLIGENCE</span></h1>
    </div>
""", unsafe_allow_html=True)

# PAGE 1: KNOWLEDGE BASE
if page == "01 / KNOWLEDGE":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<h2>DATA INGESTION</h2>", unsafe_allow_html=True)
        st.markdown("Upload project specifications and target interface. The system utilizes RAG (Retrieval-Augmented Generation) to vectorize documentation for context-aware testing.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("### DOCUMENTATION SOURCE")
        uploaded_docs = st.file_uploader("PDF / MD / TXT / JSON", accept_multiple_files=True, key="docs")
    with c2:
        st.markdown("### TARGET INTERFACE")
        uploaded_checkout = st.file_uploader("HTML SOURCE", type=["html"], key="checkout")

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    if st.button("INITIALIZE VECTOR DATABASE"):
        with st.spinner("PROCESSING..."):
            try:
                if uploaded_docs:
                    files = [("files", (f.name, f, f.type)) for f in uploaded_docs]
                    requests.post(f"{API_URL}/upload_docs", files=files)
                if uploaded_checkout:
                    files = {"file": ("checkout.html", uploaded_checkout, "text/html")}
                    requests.post(f"{API_URL}/upload_checkout", files=files)
                
                res = requests.post(f"{API_URL}/build_kb")
                if res.status_code == 200:
                    st.success("SYSTEM SYNCHRONIZED")
                else:
                    st.error(f"ERROR: {res.text}")
            except Exception as e:
                st.error(f"CONNECTION FAILURE: {e}")

# PAGE 2: TEST SCENARIOS
elif page == "02 / SCENARIOS":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<h2>SCENARIO GENERATION</h2>", unsafe_allow_html=True)
        st.markdown("Define testing parameters. The agent will synthesize positive, negative, and edge-case scenarios based on ingested knowledge.")

    st.markdown("<br>", unsafe_allow_html=True)
    
    query = st.text_input("TEST OBJECTIVE", "Generate validation tests for the discount code input field.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("GENERATE SCENARIOS"):
        with st.spinner("ANALYZING..."):
            try:
                res = requests.post(f"{API_URL}/generate_test_cases", json={"query": query})
                if res.status_code == 200:
                    st.session_state["test_cases"] = res.json().get("test_cases", [])
                else:
                    st.error(f"GENERATION FAILED: {res.text}")
            except Exception as e:
                st.error(f"CONNECTION FAILURE: {e}")

    if "test_cases" in st.session_state:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"### DETECTED SCENARIOS ({len(st.session_state['test_cases'])})")
        st.markdown("---")
        
        for i, tc in enumerate(st.session_state["test_cases"]):
            c1, c2 = st.columns([5, 1])
            with c1:
                with st.expander(f"{tc.get('test_id')}  /  {tc.get('scenario_type').upper()}  /  {tc.get('feature').upper()}", expanded=False):
                    st.markdown(f"**EXPECTED:** {tc.get('expected_result')}")
                    st.markdown("**STEPS:**")
                    for s in tc.get('steps', []):
                        st.markdown(f"- {s}")
            with c2:
                if st.button("SELECT", key=f"sel_{i}"):
                    st.session_state["selected_test_case"] = tc
                    st.success("LOCKED")

# PAGE 3: EXECUTION
elif page == "03 / EXECUTION":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<h2>CODE SYNTHESIS</h2>", unsafe_allow_html=True)
        st.markdown("Compile selected scenarios into executable Selenium/Python artifacts.")

    st.markdown("<br>", unsafe_allow_html=True)

    if "selected_test_case" not in st.session_state:
        st.info("AWAITING SCENARIO SELECTION")
    else:
        tc = st.session_state["selected_test_case"]
        
        st.markdown(f"""
        <div style='border: 1px solid #222; padding: 20px; background: #050505;'>
            <div style='color: #666; font-size: 0.8rem; letter-spacing: 1px;'>TARGET</div>
            <div style='font-family: "Teko"; font-size: 1.5rem; color: #FFF;'>{tc.get('test_id')} // {tc.get('feature').upper()}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("COMPILE ARTIFACT"):
            with st.spinner("COMPILING..."):
                try:
                    res = requests.post(f"{API_URL}/generate_script", json={"test_case": tc})
                    if res.status_code == 200:
                        st.session_state["generated_script"] = res.json().get("script")
                    else:
                        st.error(f"COMPILATION FAILED: {res.text}")
                except Exception as e:
                    st.error(f"CONNECTION FAILURE: {e}")

    if "generated_script" in st.session_state:
        st.markdown("<br>", unsafe_allow_html=True)
        st.code(st.session_state["generated_script"], language="python")
        st.download_button("DOWNLOAD ARTIFACT", st.session_state["generated_script"], "test_script.py", "text/x-python")
