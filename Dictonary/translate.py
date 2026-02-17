"""
Automate Bilingual RPA Dictionary & Smart Translator (Pro Version)
Developed by Mirza Muhammad Mobeen
Refined for Document Translation
"""

import streamlit as st
import pandas as pd
import os
import re
import io
import tempfile
from deep_translator import GoogleTranslator
from docx import Document
from pdf2docx import Converter

# ──────────────────────────────────────────────
# 1. PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Automate Keywords Dictionary",
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
    
    /* ── Direction Toggle ── */
    div[role="radiogroup"] {
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
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

    # Normalize Columns
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
    
    # Clean Data
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
    st.markdown('<p class="sidebar-title">🔤 Automate Dictionary</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.82rem;color:#94A3B8;margin-top:-4px;">Bilingual RPA Dictionary</p>', unsafe_allow_html=True)
    st.markdown("---")

    # Category Filter
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

    # Stats
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown(f'<div class="sidebar-stat"><div class="stat-num">{len(df)}</div><div class="stat-label">Terms</div></div>', unsafe_allow_html=True)
    with col_s2:
        st.markdown(f'<div class="sidebar-stat"><div class="stat-num">{df["Category"].nunique()}</div><div class="stat-label">Cats</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    view_all = st.toggle("📊 View All Data", value=False)

    st.markdown("---")
    st.markdown('<p style="text-align:center;font-size:0.75rem;color:#CBD5E1;">Developed by<br><b>Mirza Muhammad Mobeen</b></p>', unsafe_allow_html=True)


# ──────────────────────────────────────────────
# 5. TRANSLATION LOGIC (TEXT & DOCS)
# ──────────────────────────────────────────────

def smart_translate_text(text, glossary_df, direction="En_to_Jp", return_html=True):
    """
    Core translation logic. 
    return_html=True -> Returns HTML for UI display with highlighting.
    return_html=False -> Returns plain string for file saving.
    """
    if not text or not text.strip():
        return text

    # Setup Maps
    if direction == "En_to_Jp":
        src_lang, tgt_lang = 'en', 'ja'
        action_map = dict(zip(glossary_df["Action (English)"].str.lower(), glossary_df["Action (Japanese)"]))
        activity_map = dict(zip(glossary_df["Activity (English)"].str.lower(), glossary_df["Activity (Japanese)"]))
    else:
        src_lang, tgt_lang = 'ja', 'en'
        action_map = dict(zip(glossary_df["Action (Japanese)"], glossary_df["Action (English)"]))
        activity_map = dict(zip(glossary_df["Activity (Japanese)"], glossary_df["Activity (English)"]))
    
    full_map = {**action_map, **activity_map}

    # Regex to find quoted terms: "word", 'word', 「word」, 『word』
    pattern = re.compile(r'("([^"]+)")|(\'([^\']+)\')|(「([^」]+)」)|(『([^』]+)』)')
    
    placeholders = {}
    
    def replacer(match):
        if match.group(2): term = match.group(2)
        elif match.group(4): term = match.group(4)
        elif match.group(6): term = match.group(6)
        elif match.group(8): term = match.group(8)
        else: return match.group(0)

        lookup_key = term.lower() if direction == "En_to_Jp" else term
        
        if lookup_key in full_map:
            target_term = full_map[lookup_key]
            # Use unique token that won't be translated
            key = f"[ID{len(placeholders)}]" 
            placeholders[key] = target_term
            return key
        else:
            return match.group(0)

    # Substitution
    processed_text = pattern.sub(replacer, text)
    
    # Translate
    try:
        translator = GoogleTranslator(source=src_lang, target=tgt_lang)
        translated_text = translator.translate(processed_text)
    except Exception as e:
        return f"Error: {str(e)}"

    if not translated_text:
        return text

    final_text = translated_text 

    for key, term in placeholders.items():
        # Determine Bracket Style
        if direction == "En_to_Jp":
            if return_html:
                formatted_term = f"「<span class='glossary-highlight'>{term}</span>」"
            else:
                formatted_term = f"「{term}」"
        else:
            if return_html:
                formatted_term = f""" "<span class='glossary-highlight'>{term}</span>" """
            else:
                formatted_term = f'"{term}"'
        
        # Robust Replacement (handling spaces Google might add)
        escaped_key_regex = re.escape(key).replace(r"\[", r"\[\s*").replace(r"\]", r"\s*\]")
        final_text = re.sub(escaped_key_regex, formatted_term, final_text)

    return final_text

# ──────────────────────────────────────────────
# 6. DOCUMENT PROCESSING FUNCTIONS
# ──────────────────────────────────────────────
def translate_docx_file(input_file, glossary_df, direction):
    """
    Opens a DOCX, iterates paragraphs and tables, translates content,
    and returns a BytesIO object of the new file.
    """
    doc = Document(input_file)
    
    # 1. Translate Paragraphs
    for para in doc.paragraphs:
        if para.text.strip():
            # Translate the full text of the paragraph to maintain context
            translated = smart_translate_text(para.text, glossary_df, direction, return_html=False)
            para.text = translated

    # 2. Translate Tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    if para.text.strip():
                        translated = smart_translate_text(para.text, glossary_df, direction, return_html=False)
                        para.text = translated
    
    # Save to buffer
    output_buffer = io.BytesIO()
    doc.save(output_buffer)
    output_buffer.seek(0)
    return output_buffer

def convert_and_translate_pdf(input_file, glossary_df, direction):
    """
    Converts PDF to DOCX (to keep layout), translates the DOCX,
    and returns the DOCX buffer.
    """
    # Create temp files because pdf2docx requires file paths
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tf_input:
        tf_input.write(input_file.read())
        temp_input_path = tf_input.name
        
    temp_docx_path = temp_input_path.replace(".pdf", ".docx")
    
    try:
        # Convert PDF -> DOCX
        cv = Converter(temp_input_path)
        cv.convert(temp_docx_path, start=0, end=None)
        cv.close()
        
        # Translate the resulting DOCX
        with open(temp_docx_path, "rb") as f:
            docx_buffer = translate_docx_file(f, glossary_df, direction)
            
        return docx_buffer

    finally:
        # Cleanup
        if os.path.exists(temp_input_path): os.remove(temp_input_path)
        if os.path.exists(temp_docx_path): os.remove(temp_docx_path)

# ──────────────────────────────────────────────
# 7. MAIN PAGE & TABS
# ──────────────────────────────────────────────
st.markdown('<p class="hero-title">Automate Keywords Dictionary</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Bilingual Reference & Smart Translator</p>', unsafe_allow_html=True)

# TABS
tab_dict, tab_trans, tab_files = st.tabs(["📖 Dictionary Search", "🤖 Smart Translator", "📄 Document Translator"])

# ──────────────────────────────────────────────
# TAB 1: DICTIONARY SEARCH
# ──────────────────────────────────────────────
with tab_dict:
    query = st.text_input("search_input", placeholder="Search term (e.g., 'Excel', 'Browser')...", label_visibility="collapsed")
    
    filtered = df.copy()
    if selected_cats:
        filtered = filtered[filtered["Category"].isin(selected_cats)]

    if query.strip():
        q = query.strip().lower()
        cols = ["Category", "Category (Japanese)", "Action (English)", "Action (Japanese)", "Activity (English)", "Activity (Japanese)"]
        mask = pd.Series(False, index=filtered.index)
        for col in cols:
            mask = mask | filtered[col].str.lower().str.contains(q, na=False)
        filtered = filtered[mask]

    st.markdown("---")
    
    if view_all:
        st.dataframe(filtered, use_container_width=True, hide_index=True)
    else:
        if filtered.empty:
            st.markdown('<div class="no-results"><div class="emoji">🔍</div><p>No terms found.</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<span class="cat-badge" style="margin-bottom:15px;">Found {len(filtered)} terms</span>', unsafe_allow_html=True)
            display_df = filtered.head(100)
            for _, row in display_df.iterrows():
                cat = row.get("Category", "")
                cat_jp = row.get("Category (Japanese)", "")
                en_act = row.get("Action (English)", "")
                jp_act = row.get("Action (Japanese)", "")
                en_activity = row.get("Activity (English)", "")
                jp_activity = row.get("Activity (Japanese)", "")
                
                cat_display = f'{cat} <span class="cat-jp">({cat_jp})</span>' if cat_jp and cat_jp != cat else cat

                card_html = f"""
                <div class="term-card">
                    <div class="cat-badge">{cat_display}</div>
                    <div class="card-grid">
                        <div class="lang-block en-block">
                            <h4>🇬🇧 English</h4>
                            <div class="action-val">{en_act}</div>
                            <div class="activity-val">{en_activity}</div>
                        </div>
                        <div class="arrow-divider">→</div>
                        <div class="lang-block jp-block">
                            <h4>🇯🇵 Japanese</h4>
                            <div class="action-val">{jp_act}</div>
                            <div class="activity-val">{jp_activity}</div>
                        </div>
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

# ──────────────────────────────────────────────
# TAB 2: SMART TRANSLATOR (TEXT)
# ──────────────────────────────────────────────
with tab_trans:
    st.markdown("""
    <div style="background:#F0F9FF;padding:15px;border-radius:10px;border:1px solid #BAE6FD;margin-bottom:20px;">
        <strong style="color:#0072B5">🤖 Smart Detection:</strong><br>
        Put Automate terms in quotes. The app will detect them, insert the official dictionary term, 
        and format the sentence professionally.<br>
        <small style="color:#64748B">The translator preserves the formality of your input.</small>
    </div>
    """, unsafe_allow_html=True)

    # Direction Toggle
    direction_mode = st.radio(
        "Translation Direction (Text):",
        ["🇺🇸 English ➝ 🇯🇵 Japanese", "🇯🇵 Japanese ➝ 🇺🇸 English"],
        horizontal=True,
        key="text_dir"
    )
    
    if "English" in direction_mode.split("➝")[0]:
        dir_code = "En_to_Jp"
        src_label = "🇺🇸 English Input"
        tgt_label = "🇯🇵 Japanese Output"
        placeholder_txt = 'Example: Dear Team, I want to use the "Excel Open" action for the process.'
    else:
        dir_code = "Jp_to_En"
        src_label = "🇯🇵 Japanese Input"
        tgt_label = "🇺🇸 English Output"
        placeholder_txt = 'Example: 「Excel 開く」アクションを使用したいです。'

    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.subheader(src_label)
        source_text = st.text_area("Write here...", height=200, placeholder=placeholder_txt)
        btn = st.button("Translate Text", type="primary", use_container_width=True)

    with col_t2:
        st.subheader(tgt_label)
        
        if btn and source_text:
            with st.spinner("Translating..."):
                # Call Shared Logic
                html_result = smart_translate_text(source_text, df, direction=dir_code, return_html=True)
                # For copy paste, we call again or strip html (calling again is cleaner for logic sep)
                plain_result = smart_translate_text(source_text, df, direction=dir_code, return_html=False)
            
            # HTML Result (Visual)
            st.markdown(f'<div class="result-box">{html_result}</div>', unsafe_allow_html=True)
            
            # Copy Code
            st.caption("📋 Copy raw text:")
            st.code(plain_result, language=None)
            
        elif not source_text and btn:
            st.warning("Please enter text to translate.")
        else:
            st.markdown('<div class="result-box" style="color:#94A3B8;display:flex;align-items:center;justify-content:center;">Translation will appear here...</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# TAB 3: DOCUMENT TRANSLATOR
# ──────────────────────────────────────────────
with tab_files:
    st.markdown("""
    <div style="background:#FDF2F8;padding:15px;border-radius:10px;border:1px solid #FCC2D7;margin-bottom:20px;">
        <strong style="color:#BE185D">📄 File Translator (Beta):</strong><br>
        Upload <b>Word (.docx)</b> or <b>PDF (.pdf)</b> files. 
        The system will translate the content while attempting to <b>preserve the original layout</b> (tables, headers, etc.).
        <br><small>Note: PDFs will be converted to editable Word documents for the best layout preservation.</small>
    </div>
    """, unsafe_allow_html=True)

    # Direction Toggle for Files
    file_dir_mode = st.radio(
        "Translation Direction (File):",
        ["🇺🇸 English ➝ 🇯🇵 Japanese", "🇯🇵 Japanese ➝ 🇺🇸 English"],
        horizontal=True,
        key="file_dir"
    )
    
    f_dir_code = "En_to_Jp" if "English" in file_dir_mode.split("➝")[0] else "Jp_to_En"

    uploaded_file = st.file_uploader("Upload your document", type=["docx", "pdf"])

    if uploaded_file is not None:
        file_ext = uploaded_file.name.split(".")[-1].lower()
        
        st.info(f"File '{uploaded_file.name}' detected. Ready to translate.")
        
        if st.button("🚀 Start File Translation", type="primary"):
            with st.spinner("Processing document... This may take a moment to preserve layout..."):
                try:
                    output_data = None
                    out_name = f"Translated_{uploaded_file.name}"
                    
                    if file_ext == "docx":
                        output_data = translate_docx_file(uploaded_file, df, f_dir_code)
                    
                    elif file_ext == "pdf":
                        output_data = convert_and_translate_pdf(uploaded_file, df, f_dir_code)
                        out_name = out_name.replace(".pdf", ".docx") # PDFs become DOCX
                    
                    if output_data:
                        st.success("✅ Translation Complete!")
                        st.download_button(
                            label="📥 Download Translated Document",
                            data=output_data,
                            file_name=out_name,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")


# ──────────────────────────────────────────────
# 8.FOOTER
# ──────────────────────────────────────────────
st.markdown(
    '<div class="custom-footer">© 2026 | Developed by <span>Mirza Muhammad Mobeen</span></div>',
    unsafe_allow_html=True,
)
