import streamlit as st
import re
import base64

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Advanced Universal Renderer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. CUSTOM CSS INJECTION
# ==========================================
# This makes tables look professional, ensures code blocks wrap, 
# and makes large LaTeX equations scroll horizontally instead of cutting off.
CUSTOM_CSS = """
<style>
    /* Table Styling */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 0.9em;
        font-family: sans-serif;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
    }
    thead tr {
        background-color: #009879;
        color: #ffffff;
        text-align: left;
    }
    th, td {
        padding: 12px 15px;
        border: 1px solid #ddd;
    }
    tbody tr {
        border-bottom: 1px solid #dddddd;
    }
    tbody tr:nth-of-type(even) {
        background-color: rgba(0,0,0,0.05);
    }
    tbody tr:hover {
        background-color: rgba(0,152,121,0.1);
    }
    
    /* LaTeX Math Scrolling */
    .katex-display {
        overflow-x: auto;
        overflow-y: hidden;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    
    /* Text Area Styling */
    .stTextArea textarea {
        font-family: 'Courier New', Courier, monospace;
        background-color: #1e1e1e;
        color: #d4d4d4;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ==========================================
# 3. ADVANCED TEXT PREPROCESSOR
# ==========================================
def preprocess_text(text):
    """
    Cleans and prepares raw text for Streamlit's Markdown/KaTeX engine.
    Converts standard LaTeX delimiters to Streamlit-compatible delimiters.
    """
    if not text:
        return ""
    
    # Convert \[ ... \] to $$ ... $$ for block math
    text = re.sub(r'\\\[(.*?)\\\]', r'$$\1$$', text, flags=re.DOTALL)
    
    # Convert \( ... \) to $ ... $ for inline math
    text = re.sub(r'\\\((.*?)\\\)', r'$\1$', text)
    
    # Ensure \begin{equation} ... \end{equation} is wrapped in $$ for Streamlit
    # Streamlit requires math environments to be inside $$ to trigger KaTeX
    def wrap_equation(match):
        content = match.group(0)
        # If it's already inside $$, leave it alone
        return f"\n$$\n{content}\n$$\n"

    # Match \begin{...} ... \end{...} that aren't already wrapped in $$
    # Note: this is a basic heuristic for the most common environments
    environments = ['equation', 'align', 'aligned', 'gather', 'matrix', 'bmatrix', 'pmatrix']
    for env in environments:
        pattern = rf'(?<!\$\$)\n\\begin\{{{env}\}}(.*?)\\end\{{{env}\}}\n(?!\$\$)'
        text = re.sub(pattern, wrap_equation, text, flags=re.DOTALL)

    return text

# ==========================================
# 4. EXPORT FUNCTIONALITY
# ==========================================
def get_html_download_link(raw_text):
    """Generates a downloadable HTML file of the rendered text."""
    # Wrapping in basic HTML boilerplate
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Exported Render</title>
        <!-- Load KaTeX for Math -->
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; }}
            th {{ background-color: #f2f2f2; }}
            pre {{ background-color: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        </style>
    </head>
    <body>
        <div style="white-space: pre-wrap;">
{raw_text}
        </div>
    </body>
    </html>
    """
    b64 = base64.b64encode(html_content.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="rendered_document.html" style="text-decoration: none; padding: 10px 15px; background-color: #4CAF50; color: white; border-radius: 5px; font-weight: bold;">📥 Download as HTML</a>'
    return href

# ==========================================
# 5. USER INTERFACE
# ==========================================
st.title("🔬 Advanced Markdown & LaTeX Renderer")
st.markdown("Paste your raw Markdown, LaTeX, code blocks, and HTML below. The engine will instantly parse and render it into a highly formatted document.")

# --- Sidebar Controls ---
with st.sidebar:
    st.header("⚙️ Render Settings")
    view_mode = st.radio("View Layout", ["Split Screen", "Full Render Only"])
    allow_html = st.toggle("Enable Raw HTML Parsing", value=True, help="Turn this off if you are pasting untrusted text to prevent XSS.")
    enable_latex_fix = st.toggle("Auto-Fix LaTeX Delimiters", value=True, help="Automatically converts standard LaTeX formats like '\[' to Streamlit's '$$'")
    
    st.markdown("---")
    st.markdown("### Supported Formats:")
    st.markdown("- **Markdown**: Headers, Lists, Bold/Italic\n- **Tables**: GFM format\n- **Code**: Syntax highlighting\n- **LaTeX**: Inline `$E=mc^2$` and Block `$$math$$`\n- **HTML**: Standard web tags")

# --- Initialize Session State ---
if 'raw_text' not in st.session_state:
    st.session_state.raw_text = ""

# --- Layout Logic ---
if view_mode == "Split Screen":
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.subheader("📝 Raw Input")
        raw_input = st.text_area(
            "Paste text here:", 
            value=st.session_state.raw_text, 
            height=700,
            label_visibility="collapsed"
        )
        st.session_state.raw_text = raw_input
        
    with col2:
        st.subheader("✨ Live Render")
        with st.container(border=True):
            # Apply preprocessing if toggle is on
            processed_text = preprocess_text(raw_input) if enable_latex_fix else raw_input
            
            # The core rendering engine
            st.markdown(processed_text, unsafe_allow_html=allow_html)
            
            # Show empty state if nothing is typed
            if not raw_input.strip():
                st.info("Render preview will appear here...")

else: # Full Render Only Mode
    st.subheader("📝 Raw Input (Collapsible)")
    with st.expander("Click to Edit Raw Text", expanded=True if not st.session_state.raw_text else False):
        raw_input = st.text_area(
            "Paste text here:", 
            value=st.session_state.raw_text, 
            height=300,
            label_visibility="collapsed"
        )
        st.session_state.raw_text = raw_input
        
    st.markdown("---")
    st.subheader("✨ Full Width Render")
    
    processed_text = preprocess_text(raw_input) if enable_latex_fix else raw_input
    st.markdown(processed_text, unsafe_allow_html=allow_html)
    
    if not raw_input.strip():
        st.info("Render preview will appear here...")

# --- Footer & Export ---
st.markdown("---")
if st.session_state.raw_text:
    # Word count and character count metrics
    words = len(st.session_state.raw_text.split())
    chars = len(st.session_state.raw_text)
    
    m1, m2, m3 = st.columns([1, 1, 4])
    m1.metric("Word Count", words)
    m2.metric("Character Count", chars)
    m3.markdown("<br>", unsafe_allow_html=True) # spacing
    m3.markdown(get_html_download_link(processed_text), unsafe_allow_html=True)
