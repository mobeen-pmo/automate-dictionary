"""
Automate Bilingual RPA Dictionary & Smart Translator (Pro Version)
Developed by Mirza Muhammad Mobeen
Refined for: DeepL API Integration & Percentage-based Progress Indicators
"""
#Libraries
import streamlit as st
import pandas as pd
import os
import re
import io
import tempfile
import openpyxl
import time
from deep_translator import DeeplTranslator
from docx import Document
from pdf2docx import Converter

# ──────────────────────────────────────────────
# 1. PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="SCT Automate Keywords Dictionary & Translator",
    page_icon="🔤",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# 2. CUSTOM CSS
# ──────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Hide Streamlit defaults ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {background: transparent !important;}
    header [data-testid="stToolbar"] {visibility: hidden;}

    /* Force sidebar toggle */
    button[data-testid="stSidebarCollapsedControl"] {
        visibility: visible !important;
        display: flex !important;
        color: #0072B5 !important;
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        z-index: 99999 !important;
    }

    /* ── Fonts & General ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 2rem; padding-bottom: 5rem; }

    /* ── Typography ── */
    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #0072B5 0%, #00A5E0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #64748B !important;
        margin-top: 4px;
        margin-bottom: 2rem;
    }

    /* ── Inputs ── */
    div[data-testid="stTextInput"] > div > div > input,
    div[data-testid="stTextArea"] > div > div > textarea {
        font-size: 1.05rem;
        border: 2px solid #E2E8F0;
        border-radius: 14px;
        background: #FFFFFF !important;
        color: #1E293B !important;
    }
    div[data-testid="stTextInput"] > div > div > input:focus,
    div[data-testid="stTextArea"] > div > div > textarea:focus {
        border-color: #0072B5;
        box-shadow: 0 0 0 3px rgba(0, 114, 181, 0.12);
    }

    /* ── Term Card ── */
    .term-card {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .term-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 114, 181, 0.10);
        border-color: #0072B5;
    }
    .cat-badge {
        display: inline-block;
        background: #EFF6FF !important;
        color: #0072B5 !important;
        padding: 3px 12px;
        border-radius: 8px;
        font-size: 0.73rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .cat-jp { color: #E11D48 !important; font-weight: 500; margin-left: 6px; }

    /* ── Grid Layouts ── */
    .card-grid {
        display: grid;
        grid-template-columns: 1fr auto 1fr;
        gap: 0.6rem;
        align-items: start;
    }
    .lang-block h4 {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 4px;
    }
    .lang-block .action-val { font-size: 1.05rem; font-weight: 700; color: #1E293B !important; }
    .lang-block .activity-val { font-size: 0.88rem; color: #64748B !important; }
    .en-block h4 { color: #0072B5 !important; }
    .jp-block h4 { color: #E11D48 !important; }
    .arrow-divider { font-size: 1.6rem; color: #CBD5E1 !important; padding-top: 1.2rem; }

    /* ── Sidebar & Footer ── */
    section[data-testid="stSidebar"] { background: #F8FAFC !important; border-right: 1px solid #E2E8F0; }
    .sidebar-title { font-size: 1.1rem; font-weight: 700; color: #0072B5 !important; margin-bottom: 0.3rem; }
    .sidebar-stat {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sidebar-stat .stat-num { font-size: 1.8rem; font-weight: 800; color: #0072B5 !important; }
    .sidebar-stat .stat-label { font-size: 0.78rem; color: #94A3B8 !important; text-transform: uppercase; letter-spacing: 0.5px; }

    .custom-footer {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background: #F8FAFC !important; border-top: 1px solid #E2E8F0;
        text-align: center; padding: 10px 0; font-size: 0.82rem; color: #94A3B8 !important; z-index: 9999;
    }
    .custom-footer span { color: #0072B5 !important; font-weight: 600; }
    
    /* ── Translation Highlight ── */
    .glossary-highlight {
        background-color: #FFF1F2;
        color: #E11D48;
        font-weight: 800;
        padding: 2px 6px;
        border-radius: 4px;
        border: 1px solid #FECDD3;
    }
    
    /* ── Result Box ── */
    .result-box {
        background: white;
        border: 2px solid #E2E8F0;
        border-radius: 14px;
        padding: 20px;
        min-height: 150px;
        font-size: 1.1rem;
        line-height: 1.6;
        color: #334155;
        margin-bottom: 10px;
    }
    
    /* ── Progress Bar Styling ── */
    .stProgress > div > div > div > div {
        background-color: #0072B5;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────
# 3. DATA LOADING
# ──────────────────────────────────────────────
DATA_FILE = os.path.join(os.path.dirname(__file__), "Bilingual Automation Action and Activity Catalog.csv")

@st.cache_data
def load_data() -> pd.DataFrame:
    """Loads and cleans the CSV."""
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame() 

    try:
        df = pd.read_csv(DATA_FILE, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(DATA_FILE, encoding="cp932")
    except Exception:
        return pd.DataFrame()

    if "Category" not in df.columns:
        if "Category (English)" in df.columns:
            df["Category"] = df["Category (English)"]
        elif "Category (Japanese)" in df.columns:
            df["Category"] = df["Category (Japanese)"]
    
    if "Category (Japanese)" not in df.columns:
        df["Category (Japanese)"] = ""

    required_cols = [
        "Category", "Category (Japanese)", 
        "Action (English)", "Action (Japanese)", 
        "Activity (English)", "Activity (Japanese)"
    ]
    for col in required_cols:
        if col not in df.columns:
            df[col] = ""

    if "Source" in df.columns:
        df = df.drop(columns=["Source"])
        
    df = df.drop_duplicates()
    
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip().replace("nan", "")
        
    return df

df = load_data()

if df.empty:
    st.error(f"⚠️ **Error:** Data file not found. Ensure `{os.path.basename(DATA_FILE)}` is in the directory.")
    st.stop()

# ──────────────────────────────────────────────
# 4. SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="sidebar-title">🔤 SCT Automate Dictionary</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.82rem;color:#94A3B8;margin-top:-4px;">Bilingual RPA Dictionary</p>', unsafe_allow_html=True)
    st.markdown("---")

    cat_map = {} 
    for _, row in df[["Category", "Category (Japanese)"]].drop_duplicates().iterrows():
        en = row["Category"]
        jp = row["Category (Japanese)"]
        label = f"{en} ({jp})" if jp and jp != en and jp != "" else en
        cat_map[label] = en

    category_labels = sorted(cat_map.keys())
    selected_labels = st.multiselect(
        "📂 Filter by Category",
        options=category_labels,
        default=[],
        help="Leave empty to search all categories.",
    )
    selected_cats = [cat_map[lbl] for lbl in selected_labels]

    st.markdown("---")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown(f'<div class="sidebar-stat"><div class="stat-num">{len(df)}</div><div class="stat-label">Terms</div></div>', unsafe_allow_html=True)
    with col_s2:
        st.markdown(f'<div class="sidebar-stat"><div class="stat-num">{df["Category"].nunique()}</div><div class="stat-label">Cats</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    view_all = st.toggle("📊 View All Data", value=False)
    st.markdown("---")
    st.markdown('<p style="text-align:center;font-size:0.75rem;color:#CBD5E1;">Developed by<br><b>Mirza Muhammad Mobeen</b></p
