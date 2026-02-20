import streamlit as st
import re
import base64
from io import BytesIO

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
    
    /* Copy Success Animation */
    @keyframes fadeInOut {
        0% { opacity: 0; transform: translateY(-10px); }
        20% { opacity: 1; transform: translateY(0); }
        80% { opacity: 1; transform: translateY(0); }
        100% { opacity: 0; transform: translateY(-10px); }
    }
    .copy-success {
        animation: fadeInOut 2s ease-in-out;
        color: #4CAF50;
        font-weight: bold;
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
    
    text = re.sub(r'\\\[(.*?)\\\]', r'$$\1$$', text, flags=re.DOTALL)
    text = re.sub(r'\\\((.*?)\\\)', r'$\1$', text)
    
    def wrap_equation(match):
        content = match.group(0)
        return f"\n$$\n{content}\n$$\n"

    environments = ['equation', 'align', 'aligned', 'gather', 'matrix', 'bmatrix', 'pmatrix']
    for env in environments:
        pattern = rf'(?<!\$\$)\n\\begin\{{{env}\}}(.*?)\\end\{{{env}\}}\n(?!\$\$)'
        text = re.sub(pattern, wrap_equation, text, flags=re.DOTALL)

    return text

# ==========================================
# 4. EXPORT FUNCTIONALITY
# ==========================================
def generate_full_html(rendered_text, title="Exported Document"):
    """Generates a complete, self-contained HTML document with KaTeX, 
    Markdown rendering via marked.js, syntax highlighting, and professional styling."""
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    
    <!-- KaTeX for Math Rendering -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
    
    <!-- Marked.js for Markdown Rendering -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    
    <!-- Highlight.js for Code Syntax Highlighting -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/github.min.css">
    <script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js"></script>
    
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            line-height: 1.8;
            color: #333;
            background-color: #fafafa;
        }}
        h1 {{ font-size: 2em; margin: 0.8em 0 0.4em; color: #1a1a2e; border-bottom: 2px solid #009879; padding-bottom: 10px; }}
        h2 {{ font-size: 1.6em; margin: 0.7em 0 0.3em; color: #16213e; }}
        h3 {{ font-size: 1.3em; margin: 0.6em 0 0.3em; color: #1a1a2e; }}
        h4, h5, h6 {{ margin: 0.5em 0 0.2em; color: #333; }}
        p {{ margin: 0.6em 0; }}
        a {{ color: #009879; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        blockquote {{
            border-left: 4px solid #009879;
            margin: 1em 0;
            padding: 0.5em 1em;
            background-color: #f0f9f6;
            color: #555;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}
        thead tr {{ background-color: #009879; color: #fff; }}
        th, td {{ border: 1px solid #ddd; padding: 12px 15px; text-align: left; }}
        tbody tr:nth-of-type(even) {{ background-color: #f9f9f9; }}
        tbody tr:hover {{ background-color: #e8f5e9; }}
        pre {{
            background-color: #f6f8fa;
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 1em 0;
            border: 1px solid #e1e4e8;
        }}
        code {{
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
            font-size: 0.9em;
        }}
        :not(pre) > code {{
            background-color: #eff1f3;
            padding: 2px 6px;
            border-radius: 4px;
        }}
        ul, ol {{ margin: 0.5em 0; padding-left: 2em; }}
        li {{ margin: 0.3em 0; }}
        hr {{ border: none; border-top: 2px solid #e0e0e0; margin: 2em 0; }}
        img {{ max-width: 100%; height: auto; border-radius: 8px; margin: 1em 0; }}
        .katex-display {{ overflow-x: auto; overflow-y: hidden; padding: 10px 0; }}
        .header-banner {{
            background: linear-gradient(135deg, #009879 0%, #16213e 100%);
            color: white;
            padding: 20px 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }}
        .header-banner h1 {{ color: white; border: none; margin: 0; }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #999;
            font-size: 0.85em;
        }}
    </style>
</head>
<body>
    <div class="header-banner">
        <h1>📄 {title}</h1>
        <p style="opacity:0.8; margin-top:5px;">Generated by Advanced Universal Renderer</p>
    </div>

    <div id="content"></div>

    <div class="footer">
        <p>Generated on <script>document.write(new Date().toLocaleDateString())</script> &bull; Advanced Universal Renderer</p>
    </div>

    <script>
        // Raw markdown content
        const rawContent = {repr(rendered_text)};
        
        // Configure marked
        marked.setOptions({{
            gfm: true,
            breaks: true,
            highlight: function(code, lang) {{
                if (lang && hljs.getLanguage(lang)) {{
                    try {{ return hljs.highlight(code, {{ language: lang }}).value; }} catch (e) {{}}
                }}
                return hljs.highlightAuto(code).value;
            }}
        }});
        
        // Render markdown
        document.getElementById('content').innerHTML = marked.parse(rawContent);
        
        // Render KaTeX math
        document.addEventListener("DOMContentLoaded", function() {{
            renderMathInElement(document.getElementById('content'), {{
                delimiters: [
                    {{ left: "$$", right: "$$", display: true }},
                    {{ left: "$", right: "$", display: false }},
                    {{ left: "\\\\(", right: "\\\\)", display: false }},
                    {{ left: "\\\\[", right: "\\\\]", display: true }}
                ],
                throwOnError: false
            }});
            // Highlight any remaining code blocks
            document.querySelectorAll('pre code').forEach((block) => {{
                hljs.highlightElement(block);
            }});
        }});
    </script>
</body>
</html>"""
    return html_content


def generate_rich_html_for_copy(rendered_text):
    """Generates an HTML fragment optimized for clipboard copy that preserves
    rendering when pasted into rich-text editors like Google Docs, Word, Outlook, etc."""
    html_fragment = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/github.min.css">
<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js"></script>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.7; color: #333; padding: 20px; max-width: 800px; }}
h1 {{ color: #1a1a2e; border-bottom: 2px solid #009879; padding-bottom: 8px; }}
h2 {{ color: #16213e; }}
h3 {{ color: #1a1a2e; }}
table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
thead tr {{ background-color: #009879; color: #fff; }}
th, td {{ border: 1px solid #ddd; padding: 10px 14px; }}
tbody tr:nth-of-type(even) {{ background-color: #f9f9f9; }}
blockquote {{ border-left: 4px solid #009879; padding: 8px 16px; margin: 10px 0; background: #f0f9f6; }}
pre {{ background: #f6f8fa; padding: 14px; border-radius: 6px; overflow-x: auto; border: 1px solid #e1e4e8; }}
code {{ font-family: Consolas, monospace; font-size: 0.9em; }}
:not(pre) > code {{ background: #eff1f3; padding: 2px 5px; border-radius: 3px; }}
.katex-display {{ overflow-x: auto; }}
</style>
</head>
<body>
<div id="content"></div>
<script>
marked.setOptions({{ gfm: true, breaks: true, highlight: function(code, lang) {{
    if (lang && hljs.getLanguage(lang)) {{ try {{ return hljs.highlight(code, {{ language: lang }}).value; }} catch(e) {{}} }}
    return hljs.highlightAuto(code).value;
}} }});
document.getElementById('content').innerHTML = marked.parse({repr(rendered_text)});
document.addEventListener("DOMContentLoaded", function() {{
    renderMathInElement(document.getElementById('content'), {{
        delimiters: [
            {{ left: "$$", right: "$$", display: true }},
            {{ left: "$", right: "$", display: false }}
        ],
        throwOnError: false
    }});
    document.querySelectorAll('pre code').forEach((block) => {{ hljs.highlightElement(block); }});
}});
</script>
</body>
</html>"""
    return html_fragment


def generate_txt(raw_text):
    """Returns plain text (strips nothing — keeps raw markdown/latex as-is)."""
    return raw_text


def generate_md(raw_text):
    """Returns the text as a .md file content."""
    return raw_text


def generate_pdf_html(rendered_text, title="Exported Document"):
    """Generates an HTML page with a print-to-PDF button built in, 
    so the user can save a perfect PDF from the browser."""
    pdf_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/github.min.css">
    <script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js"></script>
    
    <style>
        @media print {{
            .no-print {{ display: none !important; }}
            body {{ padding: 0; margin: 0; }}
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            line-height: 1.8;
            color: #333;
        }}
        h1 {{ font-size: 2em; margin: 0.8em 0 0.4em; color: #1a1a2e; border-bottom: 2px solid #009879; padding-bottom: 8px; }}
        h2 {{ font-size: 1.5em; margin: 0.7em 0 0.3em; color: #16213e; }}
        h3 {{ font-size: 1.2em; margin: 0.6em 0 0.3em; }}
        p {{ margin: 0.5em 0; }}
        blockquote {{ border-left: 4px solid #009879; padding: 8px 16px; margin: 10px 0; background: #f0f9f6; }}
        table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
        thead tr {{ background-color: #009879; color: #fff; }}
        th, td {{ border: 1px solid #ddd; padding: 10px 14px; }}
        tbody tr:nth-of-type(even) {{ background-color: #f9f9f9; }}
        pre {{ background: #f6f8fa; padding: 14px; border-radius: 6px; overflow-x: auto; border: 1px solid #e1e4e8; }}
        code {{ font-family: Consolas, monospace; font-size: 0.9em; }}
        :not(pre) > code {{ background: #eff1f3; padding: 2px 5px; border-radius: 3px; }}
        .katex-display {{ overflow-x: auto; }}
        .print-btn {{
            position: fixed; top: 20px; right: 20px; z-index: 1000;
            background: #009879; color: white; border: none; padding: 12px 24px;
            border-radius: 8px; font-size: 1em; cursor: pointer; font-weight: bold;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}
        .print-btn:hover {{ background: #007a63; }}
        .print-instructions {{
            position: fixed; top: 70px; right: 20px; z-index: 1000;
            background: #fff3cd; color: #856404; padding: 10px 15px;
            border-radius: 6px; font-size: 0.85em; max-width: 280px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1); border: 1px solid #ffc107;
        }}
    </style>
</head>
<body>
    <button class="print-btn no-print" onclick="window.print()">🖨️ Print / Save as PDF</button>
    <div class="print-instructions no-print">
        💡 <strong>Tip:</strong> Click the button above, then choose <em>"Save as PDF"</em> as the destination in the print dialog.
    </div>

    <div id="content"></div>

    <script>
        marked.setOptions({{ gfm: true, breaks: true, highlight: function(code, lang) {{
            if (lang && hljs.getLanguage(lang)) {{ try {{ return hljs.highlight(code, {{ language: lang }}).value; }} catch(e) {{}} }}
            return hljs.highlightAuto(code).value;
        }} }});
        document.getElementById('content').innerHTML = marked.parse({repr(rendered_text)});
        document.addEventListener("DOMContentLoaded", function() {{
            renderMathInElement(document.getElementById('content'), {{
                delimiters: [
                    {{ left: "$$", right: "$$", display: true }},
                    {{ left: "$", right: "$", display: false }},
                    {{ left: "\\\\(", right: "\\\\)", display: false }},
                    {{ left: "\\\\[", right: "\\\\]", display: true }}
                ],
                throwOnError: false
            }});
            document.querySelectorAll('pre code').forEach((block) => {{ hljs.highlightElement(block); }});
        }});
    </script>
</body>
</html>"""
    return pdf_html


def generate_rst(raw_text):
    """Basic conversion of markdown to reStructuredText format."""
    text = raw_text
    
    # Convert headers: # Header -> Header\n======
    def replace_header(match):
        level = len(match.group(1))
        title = match.group(2).strip()
        chars = {1: '=', 2: '-', 3: '~', 4: '^', 5: '"'}
        underline_char = chars.get(level, '"')
        underline = underline_char * len(title)
        if level == 1:
            return f"{underline}\n{title}\n{underline}"
        return f"{title}\n{underline}"
    
    text = re.sub(r'^(#{1,5})\s+(.+)$', replace_header, text, flags=re.MULTILINE)
    
    # Bold: **text** -> **text**  (same in rst)
    # Italic: *text* -> *text*  (same in rst)
    
    # Inline code: `code` -> ``code``
    text = re.sub(r'(?<!`)`(?!`)([^`]+)(?<!`)`(?!`)', r'``\1``', text)
    
    # Links: [text](url) -> `text <url>`_
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'`\1 <\2>`_', text)
    
    # Images: ![alt](url) -> .. image:: url\n   :alt: alt
    def replace_image(match):
        alt = match.group(1)
        url = match.group(2)
        return f".. image:: {url}\n   :alt: {alt}"
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_image, text)
    
    # Horizontal rules
    text = re.sub(r'^---+$', '-' * 40, text, flags=re.MULTILINE)
    text = re.sub(r'^\*\*\*+$', '-' * 40, text, flags=re.MULTILINE)
    
    return text


def generate_latex_doc(raw_text):
    """Basic conversion of markdown text to a LaTeX document."""
    text = raw_text
    
    # Preamble
    preamble = r"""\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{booktabs}
\usepackage[margin=1in]{geometry}

\lstset{
    basicstyle=\ttfamily\small,
    breaklines=true,
    frame=single,
    backgroundcolor=\color{gray!10},
    keywordstyle=\color{blue},
    commentstyle=\color{green!60!black},
    stringstyle=\color{red}
}

\begin{document}
"""
    postamble = r"""
\end{document}"""
    
    # Convert headers
    text = re.sub(r'^# (.+)$', r'\\section{\1}', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'\\subsection{\1}', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.+)$', r'\\subsubsection{\1}', text, flags=re.MULTILINE)
    text = re.sub(r'^#### (.+)$', r'\\paragraph{\1}', text, flags=re.MULTILINE)
    
    # Bold and Italic
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\\textbf{\\textit{\1}}', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'\\textit{\1}', text)
    
    # Inline code
    text = re.sub(r'`([^`]+)`', r'\\texttt{\1}', text)
    
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\\href{\2}{\1}', text)
    
    # Code blocks
    def replace_code_block(match):
        lang = match.group(1) or ""
        code = match.group(2)
        if lang:
            return f"\\begin{{lstlisting}}[language={lang}]\n{code}\n\\end{{lstlisting}}"
        return f"\\begin{{lstlisting}}\n{code}\n\\end{{lstlisting}}"
    
    text = re.sub(r'```(\w*)\n(.*?)```', replace_code_block, text, flags=re.DOTALL)
    
    # Horizontal rules
    text = re.sub(r'^---+$', r'\\hrulefill', text, flags=re.MULTILINE)
    
    # Blockquotes
    text = re.sub(r'^> (.+)$', r'\\begin{quote}\n\1\n\\end{quote}', text, flags=re.MULTILINE)
    
    return preamble + text + postamble


# ==========================================
# 5. COPY-TO-CLIPBOARD COMPONENT
# ==========================================
def render_copy_button(rendered_text):
    """Renders a copy button that copies rich HTML to clipboard,
    so pasting into Google Docs / Word / etc. preserves formatting."""
    
    rich_html = generate_rich_html_for_copy(rendered_text)
    b64_html = base64.b64encode(rich_html.encode('utf-8')).decode('utf-8')
    
    copy_component = f"""
    <div style="position: relative; display: inline-block; width: 100%;">
        <button id="copyBtn" onclick="copyRenderedContent()" style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 10px 22px;
            border-radius: 8px;
            font-size: 0.95em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
            display: inline-flex;
            align-items: center;
            gap: 8px;
        " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 16px rgba(102,126,234,0.5)'"
           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(102,126,234,0.4)'">
            <span id="copyIcon">📋</span> <span id="copyText">Copy Rendered Content</span>
        </button>
        <span id="copyStatus" style="margin-left: 12px; font-weight: bold; opacity: 0; transition: opacity 0.3s;"></span>
    </div>
    
    <script>
    async function copyRenderedContent() {{
        const btn = document.getElementById('copyBtn');
        const icon = document.getElementById('copyIcon');
        const text = document.getElementById('copyText');
        const status = document.getElementById('copyStatus');
        
        try {{
            // Decode the base64 HTML
            const b64 = "{b64_html}";
            const htmlContent = atob(b64);
            
            // Create a temporary hidden iframe to render the HTML
            const iframe = document.createElement('iframe');
            iframe.style.position = 'fixed';
            iframe.style.left = '-9999px';
            iframe.style.top = '-9999px';
            iframe.style.width = '800px';
            iframe.style.height = '600px';
            document.body.appendChild(iframe);
            
            iframe.contentDocument.open();
            iframe.contentDocument.write(htmlContent);
            iframe.contentDocument.close();
            
            // Wait for content to render
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            const contentDiv = iframe.contentDocument.getElementById('content');
            
            if (contentDiv) {{
                const renderedHTML = contentDiv.innerHTML;
                const plainText = contentDiv.innerText;
                
                // Use Clipboard API with both HTML and plain text
                try {{
                    const clipboardItem = new ClipboardItem({{
                        'text/html': new Blob([renderedHTML], {{ type: 'text/html' }}),
                        'text/plain': new Blob([plainText], {{ type: 'text/plain' }})
                    }});
                    await navigator.clipboard.write([clipboardItem]);
                    
                    // Success feedback
                    icon.textContent = '✅';
                    text.textContent = 'Copied!';
                    status.textContent = '✨ Rich content copied — paste into Docs, Word, Outlook, etc.';
                    status.style.color = '#4CAF50';
                    status.style.opacity = '1';
                    btn.style.background = 'linear-gradient(135deg, #4CAF50 0%, #45a049 100%)';
                    
                }} catch (clipErr) {{
                    // Fallback: copy as plain text
                    await navigator.clipboard.writeText(plainText);
                    icon.textContent = '📝';
                    text.textContent = 'Copied as Text';
                    status.textContent = '⚠️ Copied as plain text (browser blocked rich copy)';
                    status.style.color = '#ff9800';
                    status.style.opacity = '1';
                    btn.style.background = 'linear-gradient(135deg, #ff9800 0%, #f57c00 100%)';
                }}
            }} else {{
                throw new Error('Content element not found');
            }}
            
            // Remove iframe
            document.body.removeChild(iframe);
            
            // Reset button after 3 seconds
            setTimeout(() => {{
                icon.textContent = '📋';
                text.textContent = 'Copy Rendered Content';
                status.style.opacity = '0';
                btn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
            }}, 3000);
            
        }} catch (err) {{
            // Final fallback
            icon.textContent = '❌';
            text.textContent = 'Copy Failed';
            status.textContent = 'Error: ' + err.message;
            status.style.color = '#f44336';
            status.style.opacity = '1';
            btn.style.background = 'linear-gradient(135deg, #f44336 0%, #d32f2f 100%)';
            
            setTimeout(() => {{
                icon.textContent = '📋';
                text.textContent = 'Copy Rendered Content';
                status.style.opacity = '0';
                btn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
            }}, 3000);
        }}
    }}
    </script>
    """
    return copy_component


# ==========================================
# 6. USER INTERFACE
# ==========================================
st.title("🔬 Advanced Markdown & LaTeX Renderer")
st.markdown("Paste your raw Markdown, LaTeX, code blocks, and HTML below. Click **Render** to parse and display the formatted document.")

# --- Sidebar Controls ---
with st.sidebar:
    st.header("⚙️ Render Settings")
    view_mode = st.radio("View Layout", ["Split Screen", "Full Render Only"])
    allow_html = st.toggle("Enable Raw HTML Parsing", value=True, help="Turn this off if you are pasting untrusted text to prevent XSS.")
    enable_latex_fix = st.toggle("Auto-Fix LaTeX Delimiters", value=True, help="Automatically converts standard LaTeX formats like '\\[' to Streamlit's '$$'")
    
    st.markdown("---")
    
    st.header("📦 Export Settings")
    export_format = st.selectbox(
        "Choose Export Format",
        ["HTML (Rich Document)", "PDF (Print-Ready)", "Plain Text (.txt)", "Markdown (.md)", "reStructuredText (.rst)", "LaTeX (.tex)"],
        index=0
    )
    export_filename = st.text_input("File Name (without extension)", value="rendered_document")
    
    st.markdown("---")
    st.markdown("### Supported Formats:")
    st.markdown(
        "- **Markdown**: Headers, Lists, Bold/Italic\n"
        "- **Tables**: GFM format\n"
        "- **Code**: Syntax highlighting\n"
        "- **LaTeX**: Inline `$E=mc^2$` and Block `$$math$$`\n"
        "- **HTML**: Standard web tags"
    )

# --- Initialize Session State ---
if 'raw_text' not in st.session_state:
    st.session_state.raw_text = ""
if 'rendered_text' not in st.session_state:
    st.session_state.rendered_text = ""
if 'is_rendered' not in st.session_state:
    st.session_state.is_rendered = False

# --- Callback for the Render Button ---
def on_render_click():
    st.session_state.raw_text = st.session_state.input_text_area
    if enable_latex_fix:
        st.session_state.rendered_text = preprocess_text(st.session_state.raw_text)
    else:
        st.session_state.rendered_text = st.session_state.raw_text
    st.session_state.is_rendered = True

# --- Callback for the Clear Button ---
def on_clear_click():
    st.session_state.raw_text = ""
    st.session_state.rendered_text = ""
    st.session_state.is_rendered = False
    st.session_state.input_text_area = ""

# --- Layout Logic ---
if view_mode == "Split Screen":
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.subheader("📝 Raw Input")
        st.text_area(
            "Paste text here:", 
            value=st.session_state.raw_text, 
            height=600,
            label_visibility="collapsed",
            key="input_text_area"
        )
        
        btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 3])
        with btn_col1:
            st.button("🚀 Render", on_click=on_render_click, type="primary", use_container_width=True)
        with btn_col2:
            st.button("🗑️ Clear", on_click=on_clear_click, use_container_width=True)
        
    with col2:
        st.subheader("✨ Rendered Output")
        with st.container(border=True):
            if st.session_state.is_rendered and st.session_state.rendered_text.strip():
                st.markdown(st.session_state.rendered_text, unsafe_allow_html=allow_html)
            else:
                st.info("✏️ Paste your text on the left and click **🚀 Render** to see the output here.")

else:  # Full Render Only Mode
    st.subheader("📝 Raw Input")
    with st.expander("Click to Edit Raw Text", expanded=not st.session_state.is_rendered):
        st.text_area(
            "Paste text here:", 
            value=st.session_state.raw_text, 
            height=300,
            label_visibility="collapsed",
            key="input_text_area"
        )
        
        btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 5])
        with btn_col1:
            st.button("🚀 Render", on_click=on_render_click, type="primary", use_container_width=True)
        with btn_col2:
            st.button("🗑️ Clear", on_click=on_clear_click, use_container_width=True)
        
    st.markdown("---")
    st.subheader("✨ Full Width Render")
    
    if st.session_state.is_rendered and st.session_state.rendered_text.strip():
        st.markdown(st.session_state.rendered_text, unsafe_allow_html=allow_html)
    else:
        st.info("✏️ Paste your text above and click **🚀 Render** to see the output here.")

# ==========================================
# 7. FOOTER: COPY, EXPORT & METRICS
# ==========================================
st.markdown("---")

if st.session_state.is_rendered and st.session_state.rendered_text.strip():
    
    # --- Copy Button Section ---
    st.subheader("📋 Copy Rendered Content")
    st.caption("Click below to copy the fully rendered content to your clipboard. When you paste it into Google Docs, Word, Outlook, or any rich-text editor, the formatting (headings, tables, code, math) will be preserved.")
    st.components.v1.html(render_copy_button(st.session_state.rendered_text), height=60)
    
    st.markdown("---")
    
    # --- Export Section ---
    st.subheader("📦 Download Exported File")
    
    rendered = st.session_state.rendered_text
    raw = st.session_state.raw_text
    fname = export_filename if export_filename.strip() else "rendered_document"
    
    if export_format == "HTML (Rich Document)":
        file_content = generate_full_html(rendered, title=fname)
        file_bytes = file_content.encode('utf-8')
        file_ext = "html"
        mime = "text/html"
        description = "A fully self-contained HTML file with KaTeX math rendering, syntax-highlighted code blocks, styled tables, and professional formatting. Opens in any browser."
        
    elif export_format == "PDF (Print-Ready)":
        file_content = generate_pdf_html(rendered, title=fname)
        file_bytes = file_content.encode('utf-8')
        file_ext = "html"
        mime = "text/html"
        description = "An HTML file with a built-in **Print / Save as PDF** button. Open the downloaded file in your browser, click the button, and choose 'Save as PDF' in the print dialog. This ensures perfect rendering of math, code, and tables."
        
    elif export_format == "Plain Text (.txt)":
        file_content = generate_txt(raw)
        file_bytes = file_content.encode('utf-8')
        file_ext = "txt"
        mime = "text/plain"
        description = "A plain text file containing the raw content as-is. No formatting is applied."
        
    elif export_format == "Markdown (.md)":
        file_content = generate_md(raw)
        file_bytes = file_content.encode('utf-8')
        file_ext = "md"
        mime = "text/markdown"
        description = "A Markdown (.md) file that can be opened in any Markdown editor or viewer (VS Code, Typora, Obsidian, GitHub, etc.)."
        
    elif export_format == "reStructuredText (.rst)":
        file_content = generate_rst(raw)
        file_bytes = file_content.encode('utf-8')
        file_ext = "rst"
        mime = "text/x-rst"
        description = "A reStructuredText file commonly used in Python documentation (Sphinx). Basic conversion from Markdown is applied."
        
    elif export_format == "LaTeX (.tex)":
        file_content = generate_latex_doc(raw)
        file_bytes = file_content.encode('utf-8')
        file_ext = "tex"
        mime = "application/x-tex"
        description = "A LaTeX (.tex) document with standard preamble. Can be compiled with pdflatex, xelatex, or lualatex. Includes packages for math, code listings, hyperlinks, and tables."
    
    st.info(f"📄 **{export_format}**: {description}")
    
    dl_col1, dl_col2 = st.columns([1, 4])
    with dl_col1:
        st.download_button(
            label=f"📥 Download .{file_ext}",
            data=file_bytes,
            file_name=f"{fname}.{file_ext}",
            mime=mime,
            type="primary",
            use_container_width=True
        )
    with dl_col2:
        st.caption(f"File: `{fname}.{file_ext}` | Size: {len(file_bytes):,} bytes | Format: {export_format}")
    
    st.markdown("---")
    
    # --- Metrics ---
    st.subheader("📊 Document Statistics")
    words = len(st.session_state.raw_text.split())
    chars = len(st.session_state.raw_text)
    lines = st.session_state.raw_text.count('\n') + 1
    code_blocks = len(re.findall(r'```', st.session_state.raw_text)) // 2
    math_inline = len(re.findall(r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)', st.session_state.raw_text))
    math_block = len(re.findall(r'\$\$', st.session_state.raw_text)) // 2
    tables = len(re.findall(r'^\|(.+\|)+$', st.session_state.raw_text, re.MULTILINE))
    headers = len(re.findall(r'^#{1,6}\s', st.session_state.raw_text, re.MULTILINE))
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📝 Words", f"{words:,}")
    m2.metric("🔤 Characters", f"{chars:,}")
    m3.metric("📄 Lines", f"{lines:,}")
    m4.metric("📑 Headers", headers)
    
    m5, m6, m7, m8 = st.columns(4)
    m5.metric("💻 Code Blocks", code_blocks)
    m6.metric("🔢 Inline Math", math_inline)
    m7.metric("📐 Block Math", math_block)
    m8.metric("📊 Table Rows", tables)
