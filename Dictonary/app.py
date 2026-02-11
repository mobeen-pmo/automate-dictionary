"""
Automate Bilingual RPA Dictionary
Developed by Mirza Muhammad Mobeen
"""

import streamlit as st
import pandas as pd
import os

# ──────────────────────────────────────────────
# 1. PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Automate Keywords Dictonary",
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
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* ── Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Page padding ── */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    /* ── Hero header ── */
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
        color: #64748B;
        margin-top: 4px;
        margin-bottom: 2rem;
    }

    /* ── Search bar ── */
    div[data-testid="stTextInput"] > div > div > input {
        font-size: 1.1rem;
        padding: 0.85rem 1.2rem;
        border: 2px solid #E2E8F0;
        border-radius: 14px;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="stTextInput"] > div > div > input:focus {
        border-color: #0072B5;
        box-shadow: 0 0 0 3px rgba(0, 114, 181, 0.12);
    }

    /* ── Results badge ── */
    .results-badge {
        display: inline-block;
        background: linear-gradient(135deg, #0072B5 0%, #00A5E0 100%);
        color: white;
        padding: 6px 18px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 1.2rem;
        letter-spacing: 0.3px;
    }

    /* ── Term Card ── */
    .term-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        position: relative;
    }
    .term-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 114, 181, 0.10);
        border-color: #0072B5;
    }

    /* ── Category pill ── */
    .cat-badge {
        display: inline-block;
        background: #EFF6FF;
        color: #0072B5;
        padding: 3px 12px;
        border-radius: 8px;
        font-size: 0.73rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 1rem;
    }

    /* ── Card inner grid ── */
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
    .lang-block .action-val {
        font-size: 1.05rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 6px;
    }
    .lang-block .activity-val {
        font-size: 0.88rem;
        color: #64748B;
        line-height: 1.5;
    }
    .en-block h4 { color: #0072B5; }
    .jp-block h4 { color: #E11D48; }
    .jp-block .action-val { color: #1E293B; }

    /* ── Arrow divider ── */
    .arrow-divider {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.6rem;
        color: #CBD5E1;
        padding: 0 0.4rem;
        padding-top: 1.2rem;
    }

    /* ── Sidebar styling ── */
    section[data-testid="stSidebar"] {
        background: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    .sidebar-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0072B5;
        margin-bottom: 0.3rem;
    }
    .sidebar-stat {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sidebar-stat .stat-num {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0072B5;
    }
    .sidebar-stat .stat-label {
        font-size: 0.78rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* ── Fixed footer ── */
    .custom-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #F8FAFC;
        border-top: 1px solid #E2E8F0;
        text-align: center;
        padding: 10px 0;
        font-size: 0.82rem;
        color: #94A3B8;
        z-index: 9999;
        letter-spacing: 0.3px;
    }
    .custom-footer span {
        color: #0072B5;
        font-weight: 600;
    }

    /* ── No results ── */
    .no-results {
        text-align: center;
        padding: 3rem 1rem;
        color: #94A3B8;
    }
    .no-results .emoji {
        font-size: 3rem;
        margin-bottom: 0.5rem;
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
    """Load and clean the bilingual catalog CSV."""
    try:
        df = pd.read_csv(DATA_FILE, encoding="utf-8")
    except UnicodeDecodeError:
        # Fallback for Windows-coded files
        df = pd.read_csv(DATA_FILE, encoding="cp932")

    # Normalize column names
    # The app expects: Category, Action (English), Action (Japanese), Activity (English), Activity (Japanese)
    # The CSV provided has: Category (English), Category (Japanese), Activity (English), Activity (Japanese)
    
    # 1. Map Category
    if "Category" not in df.columns:
        if "Category (English)" in df.columns:
            df["Category"] = df["Category (English)"]
        elif "Category (Japanese)" in df.columns:
            df["Category"] = df["Category (Japanese)"]
    
    # 2. Ensure Action/Activity columns exist
    # If Action is missing but Activity exists, we keep Activity.
    # We just ensure the columns referenced in SEARCH_COLS and the UI exist.
    required_cols = [
        "Category",
        "Action (English)",
        "Action (Japanese)",
        "Activity (English)",
        "Activity (Japanese)"
    ]
    
    for col in required_cols:
        if col not in df.columns:
            df[col] = ""

    # Drop the Source column — not needed in search UI
    if "Source" in df.columns:
        df = df.drop(columns=["Source"])
        
    # Remove duplicate rows so each term appears only once
    df = df.drop_duplicates()
    
    # Clean whitespace & fill blanks
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip().replace("nan", "")
        
    return df


df = load_data()

SEARCH_COLS = [
    "Action (English)",
    "Action (Japanese)",
    "Activity (English)",
    "Activity (Japanese)",
]

# ──────────────────────────────────────────────
# 4. SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="sidebar-title">🔤 Automate Keywords Dictonary </p>', unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size:0.82rem;color:#94A3B8;margin-top:-4px;">'
        "Bilingual RPA Dictionary</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # Category filter
    categories = sorted(df["Category"].unique())
    selected_cats = st.multiselect(
        "📂 Filter by Category",
        options=categories,
        default=[],
        help="Leave empty to search all categories.",
    )

    st.markdown("---")

    # Quick stats
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown(
            f'<div class="sidebar-stat">'
            f'<div class="stat-num">{len(df)}</div>'
            f'<div class="stat-label">Terms</div></div>',
            unsafe_allow_html=True,
        )
    with col_s2:
        st.markdown(
            f'<div class="sidebar-stat">'
            f'<div class="stat-num">{df["Category"].nunique()}</div>'
            f'<div class="stat-label">Categories</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    view_all = st.toggle("📊 View All Data", value=False)

    st.markdown("---")
    st.markdown(
        '<p style="text-align:center;font-size:0.75rem;color:#CBD5E1;">'
        "Developed by<br><b>Mirza Muhammad Mobeen</b></p>",
        unsafe_allow_html=True,
    )

# ──────────────────────────────────────────────
# 5. MAIN HEADER
# ──────────────────────────────────────────────
st.markdown('<p class="hero-title">Automate Keywords Dictonary </p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-subtitle">'
    "Your bilingual reference for RPA Actions & Activities — English ↔ Japanese"
    "</p>",
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────
# 6. SEARCH BAR
# ──────────────────────────────────────────────
query = st.text_input(
    "search_input",
    placeholder="Search any term (e.g., 'Excel', 'Browser', 'Click')...",
    label_visibility="collapsed",
)

# ──────────────────────────────────────────────
# 7. FILTER & SEARCH
# ──────────────────────────────────────────────
filtered = df.copy()

# Apply category filter
if selected_cats:
    filtered = filtered[filtered["Category"].isin(selected_cats)]

# Apply text search
if query.strip():
    q = query.strip().lower()
    mask = pd.Series(False, index=filtered.index)
    for col in SEARCH_COLS:
        mask = mask | filtered[col].str.lower().str.contains(q, na=False)
    filtered = filtered[mask]

# ──────────────────────────────────────────────
# 8. VIEW ALL MODE (raw dataframe)
# ──────────────────────────────────────────────
if view_all:
    st.markdown("---")
    st.markdown(
        f'<span class="results-badge">📋 Showing all {len(filtered)} terms</span>',
        unsafe_allow_html=True,
    )
    st.dataframe(filtered, use_container_width=True, hide_index=True)

# ──────────────────────────────────────────────
# 9. CARD DISPLAY
# ──────────────────────────────────────────────
else:
    st.markdown("---")

    if query.strip() or selected_cats:
        st.markdown(
            f'<span class="results-badge">🔍 Found {len(filtered)} matching term{"s" if len(filtered) != 1 else ""}</span>',
            unsafe_allow_html=True,
        )

    if filtered.empty:
        st.markdown(
            '<div class="no-results">'
            '<div class="emoji">🔍</div>'
            "<p>No matching terms found. Try a different search or clear filters.</p>"
            "</div>",
            unsafe_allow_html=True,
        )
    else:
        # Render cards
        display_df = filtered.head(100)  # cap for performance
        for _, row in display_df.iterrows():
            cat = row.get("Category", "")
            en_action = row.get("Action (English)", "")
            jp_action = row.get("Action (Japanese)", "")
            en_activity = row.get("Activity (English)", "")
            jp_activity = row.get("Activity (Japanese)", "")

            card_html = f"""
            <div class="term-card">
                <div class="cat-badge">{cat}</div>
                <div class="card-grid">
                    <div class="lang-block en-block">
                        <h4>🇬🇧 English</h4>
                        <div class="action-val">{en_action}</div>
                        <div class="activity-val">{en_activity}</div>
                    </div>
                    <div class="arrow-divider">→</div>
                    <div class="lang-block jp-block">
                        <h4>🇯🇵 Japanese</h4>
                        <div class="action-val">{jp_action}</div>
                        <div class="activity-val">{jp_activity}</div>
                    </div>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

        if len(filtered) > 100:
            st.info(
                f"Showing first 100 of {len(filtered)} results. "
                "Use the search bar or category filter to narrow down."
            )

# ──────────────────────────────────────────────
# 10. FIXED FOOTER
# ──────────────────────────────────────────────
st.markdown(
    '<div class="custom-footer">'
    "© 2025 | Developed by <span>Mirza Muhammad Mobeen</span>"
    "</div>",
    unsafe_allow_html=True,
)
