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
# 2. CUSTOM CSS INJECTION (Minimal - No color forcing)
# ==========================================
CUSTOM_CSS = """
<style>
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
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ==========================================
# 3. ADVANCED TEXT PREPROCESSOR
# ==========================================
def preprocess_text(text):
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
# 4. EXPORT GENERATORS
# ==========================================
def generate_full_html(rendered_text, title="Exported Document"):
    """Clean HTML with no forced colors — inherits natural browser defaults."""
    html_content = f"""<!DOCTYPE html>
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
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            line-height: 1.8;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ccc;
            padding: 10px 14px;
            text-align: left;
        }}
        pre {{
            background-color: #f6f8fa;
            padding: 16px;
            border-radius: 6px;
            overflow-x: auto;
            border: 1px solid #e1e4e8;
        }}
        code {{
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
            font-size: 0.9em;
        }}
        :not(pre) > code {{
            background-color: #f0f0f0;
            padding: 2px 6px;
            border-radius: 4px;
        }}
        blockquote {{
            border-left: 4px solid #ccc;
            margin: 1em 0;
            padding: 0.5em 1em;
        }}
        img {{ max-width: 100%; height: auto; }}
        .katex-display {{ overflow-x: auto; overflow-y: hidden; padding: 10px 0; }}
        hr {{ border: none; border-top: 1px solid #ccc; margin: 2em 0; }}

        @media print {{
            .no-print {{ display: none !important; }}
        }}
        .pdf-btn {{
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            background: #333;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-size: 0.95em;
            cursor: pointer;
            font-weight: bold;
        }}
        .pdf-btn:hover {{ background: #555; }}
        .pdf-tip {{
            position: fixed;
            top: 65px;
            right: 20px;
            z-index: 1000;
            background: #fffbe6;
            padding: 8px 14px;
            border-radius: 6px;
            font-size: 0.82em;
            max-width: 260px;
            border: 1px solid #e0d080;
        }}
    </style>
</head>
<body>
    <button class="pdf-btn no-print" onclick="window.print()">🖨️ Print / Save as PDF</button>
    <div class="pdf-tip no-print">💡 Click the button, then choose <em>"Save as PDF"</em> in the print dialog.</div>

    <div id="content"></div>

    <script>
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
            document.querySelectorAll('pre code').forEach((block) => {{
                hljs.highlightElement(block);
            }});
        }});
    </script>
</body>
</html>"""
    return html_content


def generate_pdf_via_js(rendered_text, title="Exported Document"):
    """HTML page that auto-generates a PDF using html2pdf.js and also allows manual save."""
    html_content = f"""<!DOCTYPE html>
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
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <style>
        @media print {{
            .no-print {{ display: none !important; }}
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            line-height: 1.8;
        }}
        table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
        th, td {{ border: 1px solid #ccc; padding: 10px 14px; text-align: left; }}
        pre {{ background: #f6f8fa; padding: 14px; border-radius: 6px; overflow-x: auto; border: 1px solid #e1e4e8; }}
        code {{ font-family: Consolas, monospace; font-size: 0.9em; }}
        :not(pre) > code {{ background: #f0f0f0; padding: 2px 5px; border-radius: 3px; }}
        blockquote {{ border-left: 4px solid #ccc; padding: 8px 16px; margin: 10px 0; }}
        img {{ max-width: 100%; height: auto; }}
        .katex-display {{ overflow-x: auto; }}
        hr {{ border: none; border-top: 1px solid #ccc; margin: 2em 0; }}

        .toolbar {{
            position: fixed;
            top: 0; left: 0; right: 0;
            background: #f8f8f8;
            border-bottom: 1px solid #ddd;
            padding: 12px 20px;
            display: flex;
            gap: 12px;
            align-items: center;
            z-index: 9999;
            flex-wrap: wrap;
        }}
        .toolbar button {{
            background: #333;
            color: white;
            border: none;
            padding: 8px 18px;
            border-radius: 6px;
            font-size: 0.9em;
            cursor: pointer;
            font-weight: bold;
        }}
        .toolbar button:hover {{ background: #555; }}
        .toolbar .status {{
            font-size: 0.85em;
            margin-left: 10px;
        }}
        #content {{ margin-top: 70px; }}
    </style>
</head>
<body>
    <div class="toolbar no-print">
        <button onclick="downloadPDF()">📥 Download as PDF</button>
        <button onclick="window.print()">🖨️ Print / Save as PDF</button>
        <span class="status" id="status"></span>
    </div>

    <div id="content"></div>

    <script>
        marked.setOptions({{
            gfm: true,
            breaks: true,
            highlight: function(code, lang) {{
                if (lang && hljs.getLanguage(lang)) {{
                    try {{ return hljs.highlight(code, {{ language: lang }}).value; }} catch(e) {{}}
                }}
                return hljs.highlightAuto(code).value;
            }}
        }});
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
            document.querySelectorAll('pre code').forEach((block) => {{
                hljs.highlightElement(block);
            }});
        }});

        function downloadPDF() {{
            const status = document.getElementById('status');
            status.textContent = '⏳ Generating PDF... please wait.';
            status.style.color = '#333';

            const element = document.getElementById('content');
            const opt = {{
                margin:       [10, 10, 10, 10],
                filename:     '{title}.pdf',
                image:        {{ type: 'jpeg', quality: 0.98 }},
                html2canvas:  {{ scale: 2, useCORS: true, logging: false }},
                jsPDF:        {{ unit: 'mm', format: 'a4', orientation: 'portrait' }},
                pagebreak:    {{ mode: ['avoid-all', 'css', 'legacy'] }}
            }};

            html2pdf().set(opt).from(element).save().then(function() {{
                status.textContent = '✅ PDF downloaded!';
                status.style.color = 'green';
                setTimeout(() => {{ status.textContent = ''; }}, 3000);
            }}).catch(function(err) {{
                status.textContent = '❌ Error: ' + err.message;
                status.style.color = 'red';
            }});
        }}
    </script>
</body>
</html>"""
    return html_content


def generate_rich_html_for_copy(rendered_text):
    """Generates clean HTML for clipboard copy — no forced colors."""
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
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.7; padding: 20px; max-width: 800px; }}
table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
th, td {{ border: 1px solid #ccc; padding: 10px 14px; }}
blockquote {{ border-left: 4px solid #ccc; padding: 8px 16px; margin: 10px 0; }}
pre {{ background: #f6f8fa; padding: 14px; border-radius: 6px; overflow-x: auto; border: 1px solid #e1e4e8; }}
code {{ font-family: Consolas, monospace; font-size: 0.9em; }}
:not(pre) > code {{ background: #f0f0f0; padding: 2px 5px; border-radius: 3px; }}
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
    return raw_text


def generate_md(raw_text):
    return raw_text


def generate_rst(raw_text):
    text = raw_text
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
    text = re.sub(r'(?<!`)`(?!`)([^`]+)(?<!`)`(?!`)', r'``\1``', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'`\1 <\2>`_', text)
    def replace_image(match):
        alt = match.group(1)
        url = match.group(2)
        return f".. image:: {url}\n   :alt: {alt}"
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_image, text)
    text = re.sub(r'^---+$', '-' * 40, text, flags=re.MULTILINE)
    text = re.sub(r'^\*\*\*+$', '-' * 40, text, flags=re.MULTILINE)
    return text


def generate_latex_doc(raw_text):
    text = raw_text
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
    text = re.sub(r'^# (.+)$', r'\\section{\1}', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'\\subsection{\1}', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.+)$', r'\\subsubsection{\1}', text, flags=re.MULTILINE)
    text = re.sub(r'^#### (.+)$', r'\\paragraph{\1}', text, flags=re.MULTILINE)
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\\textbf{\\textit{\1}}', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'\\textit{\1}', text)
    text = re.sub(r'`([^`]+)`', r'\\texttt{\1}', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\\href{\2}{\1}', text)
    def replace_code_block(match):
        lang = match.group(1) or ""
        code = match.group(2)
        if lang:
            return f"\\begin{{lstlisting}}[language={lang}]\n{code}\n\\end{{lstlisting}}"
        return f"\\begin{{lstlisting}}\n{code}\n\\end{{lstlisting}}"
    text = re.sub(r'```(\w*)\n(.*?)```', replace_code_block, text, flags=re.DOTALL)
    text = re.sub(r'^---+$', r'\\hrulefill', text, flags=re.MULTILINE)
    text = re.sub(r'^> (.+)$', r'\\begin{quote}\n\1\n\\end{quote}', text, flags=re.MULTILINE)
    return preamble + text + postamble


# ==========================================
# 5. PDF GENERATION (Direct in Streamlit)
# ==========================================
def generate_pdf_bytes(rendered_text, title="Exported Document"):
    """
    Attempts to generate a real PDF using available libraries.
    Falls back gracefully with clear user guidance.
    """
    try:
        from fpdf import FPDF
        
        class PDF(FPDF):
            def header(self):
                self.set_font('Helvetica', 'B', 14)
                self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT", align='C')
                self.ln(5)
            
            def footer(self):
                self.set_y(-15)
                self.set_font('Helvetica', 'I', 8)
                self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')
        
        pdf = PDF()
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        lines = rendered_text.split('\n')
        for line in lines:
            stripped = line.strip()
            
            if stripped.startswith('# '):
                pdf.set_font('Helvetica', 'B', 18)
                pdf.multi_cell(0, 10, stripped[2:])
                pdf.ln(3)
            elif stripped.startswith('## '):
                pdf.set_font('Helvetica', 'B', 15)
                pdf.multi_cell(0, 9, stripped[3:])
                pdf.ln(2)
            elif stripped.startswith('### '):
                pdf.set_font('Helvetica', 'B', 13)
                pdf.multi_cell(0, 8, stripped[4:])
                pdf.ln(2)
            elif stripped.startswith('#### '):
                pdf.set_font('Helvetica', 'B', 12)
                pdf.multi_cell(0, 7, stripped[5:])
                pdf.ln(1)
            elif stripped.startswith('---') or stripped.startswith('***'):
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                pdf.ln(5)
            elif stripped.startswith('> '):
                pdf.set_font('Helvetica', 'I', 11)
                pdf.set_x(20)
                pdf.multi_cell(170, 7, stripped[2:])
                pdf.ln(2)
                pdf.set_font('Helvetica', '', 11)
            elif stripped.startswith('- ') or stripped.startswith('* '):
                pdf.set_font('Helvetica', '', 11)
                pdf.set_x(15)
                pdf.multi_cell(175, 7, f"  •  {stripped[2:]}")
            elif re.match(r'^\d+\.\s', stripped):
                pdf.set_font('Helvetica', '', 11)
                pdf.set_x(15)
                pdf.multi_cell(175, 7, f"  {stripped}")
            elif stripped.startswith('```'):
                pdf.set_font('Courier', '', 9)
            elif stripped == '':
                pdf.ln(3)
            else:
                clean = re.sub(r'\*\*\*(.+?)\*\*\*', r'\1', stripped)
                clean = re.sub(r'\*\*(.+?)\*\*', r'\1', clean)
                clean = re.sub(r'\*(.+?)\*', r'\1', clean)
                clean = re.sub(r'`(.+?)`', r'\1', clean)
                clean = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', clean)
                clean = re.sub(r'\$\$(.+?)\$\$', r'[Math: \1]', clean)
                clean = re.sub(r'\$(.+?)\$', r'\1', clean)
                
                pdf.set_font('Helvetica', '', 11)
                try:
                    pdf.multi_cell(0, 7, clean)
                except Exception:
                    safe = clean.encode('latin-1', 'replace').decode('latin-1')
                    pdf.multi_cell(0, 7, safe)
        
        return pdf.output()
    
    except ImportError:
        pass
    
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import mm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                                leftMargin=20*mm, rightMargin=20*mm,
                                topMargin=20*mm, bottomMargin=20*mm)
        styles = getSampleStyleSheet()
        story = []
        
        for line in rendered_text.split('\n'):
            stripped = line.strip()
            if stripped.startswith('# '):
                story.append(Paragraph(stripped[2:], styles['Heading1']))
            elif stripped.startswith('## '):
                story.append(Paragraph(stripped[3:], styles['Heading2']))
            elif stripped.startswith('### '):
                story.append(Paragraph(stripped[4:], styles['Heading3']))
            elif stripped == '':
                story.append(Spacer(1, 6*mm))
            else:
                clean = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', stripped)
                clean = re.sub(r'\*(.+?)\*', r'<i>\1</i>', clean)
                clean = re.sub(r'`(.+?)`', r'<font face="Courier">\1</font>', clean)
                try:
                    story.append(Paragraph(clean, styles['BodyText']))
                except Exception:
                    story.append(Paragraph(stripped, styles['BodyText']))
        
        doc.build(story)
        return buffer.getvalue()
    
    except ImportError:
        pass
    
    return None


# ==========================================
# 6. COPY BUTTON COMPONENT (FIXED: UTF-8 + KaTeX + bold)
# ==========================================
def render_copy_button(rendered_text):
    rich_html = generate_rich_html_for_copy(rendered_text)
    b64_html = base64.b64encode(rich_html.encode('utf-8')).decode('utf-8')
    
    copy_component = f"""
    <div style="position: relative; display: inline-block; width: 100%;">
        <button id="copyBtn" onclick="copyRenderedContent()" style="
            background: #333;
            color: white;
            border: none;
            padding: 10px 22px;
            border-radius: 8px;
            font-size: 0.95em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        " onmouseover="this.style.background='#555'"
           onmouseout="this.style.background='#333'">
            <span id="copyIcon">📋</span> <span id="copyText">Copy Rendered Content</span>
        </button>
        <span id="copyStatus" style="margin-left: 12px; font-weight: bold; opacity: 0; transition: opacity 0.3s;"></span>
    </div>
    
    <script>
    /* ---- UTF-8 safe base64 decoder ---- */
    function b64DecodeUnicode(base64str) {{
        var binaryStr = atob(base64str);
        var bytes = new Uint8Array(binaryStr.length);
        for (var i = 0; i < binaryStr.length; i++) {{
            bytes[i] = binaryStr.charCodeAt(i);
        }}
        return new TextDecoder('utf-8').decode(bytes);
    }}

    /* ---- Clean DOM for Google Docs paste ---- */
    function cleanForGoogleDocs(containerEl) {{
        var clone = containerEl.cloneNode(true);

        /* --- A. Replace KaTeX DISPLAY math with plain LaTeX source --- */
        var displayEls = clone.querySelectorAll('.katex-display');
        for (var i = 0; i < displayEls.length; i++) {{
            var el = displayEls[i];
            var annotation = el.querySelector('annotation[encoding="application/x-tex"]');
            var p = document.createElement('p');
            p.style.fontFamily = '"Courier New", Courier, monospace';
            p.style.fontWeight = 'normal';
            p.style.whiteSpace = 'pre-wrap';
            p.style.margin = '10px 0';
            p.textContent = annotation ? annotation.textContent.trim() : (el.textContent || '').trim();
            el.parentNode.replaceChild(p, el);
        }}

        /* --- B. Replace INLINE KaTeX with plain LaTeX source --- */
        var inlineEls = clone.querySelectorAll('.katex');
        for (var j = 0; j < inlineEls.length; j++) {{
            var iel = inlineEls[j];
            var ann = iel.querySelector('annotation[encoding="application/x-tex"]');
            var span = document.createElement('span');
            span.style.fontFamily = '"Courier New", Courier, monospace';
            span.style.fontWeight = 'normal';
            span.textContent = ann ? ann.textContent.trim() : (iel.textContent || '').trim();
            iel.parentNode.replaceChild(span, iel);
        }}

        /* --- C. Remove leftover KaTeX internals --- */
        var junkSelectors = '.katex-mathml, .katex-html, .strut, .mspace, .vlist, .vlist-t, .vlist-t2, .vlist-r, .vlist-s, .pstrut, .frac-line, .sizing, .reset-size, .mtight';
        var junkEls = clone.querySelectorAll(junkSelectors);
        for (var k = junkEls.length - 1; k >= 0; k--) {{
            var junk = junkEls[k];
            while (junk.firstChild) {{
                junk.parentNode.insertBefore(junk.firstChild, junk);
            }}
            junk.parentNode.removeChild(junk);
        }}

        /* --- D. Strip invisible Unicode characters --- */
        var walker = document.createTreeWalker(clone, NodeFilter.SHOW_TEXT, null, false);
        while (walker.nextNode()) {{
            walker.currentNode.nodeValue = walker.currentNode.nodeValue
                .replace(/[\\u200B\\u200C\\u200D\\u2060\\uFEFF\\uFFFC\\uFFFD]/g, '')
                .replace(/\\u00A0/g, ' ');
        }}

        /* =========================================================
           E. FIX BOLD: Explicitly set font-weight on every element.
              Google Docs ignores CSS classes/stylesheets — it only
              respects inline styles.  Without explicit font-weight,
              Docs guesses (often wrong → everything bold).
              
              Strategy:
              - Root wrapper + every BLOCK element → font-weight:normal
              - <strong>, <b>, <th>, <h1>-<h6>  → font-weight:bold
              - Inline elements (<span>, <em>, <a>, <code>) are LEFT
                ALONE so they correctly inherit from their parent
                (bold inside <strong>, normal inside <p>).
           ========================================================= */

        /* E1. Root container: default = normal */
        clone.style.fontWeight = 'normal';
        clone.style.fontFamily = 'Arial, sans-serif';
        clone.style.fontSize = '11pt';
        clone.style.lineHeight = '1.6';

        /* E2. All block-level elements: explicitly normal */
        var blockTags = clone.querySelectorAll('p, li, td, div, blockquote, pre, ul, ol, dl, dd, dt, address, figcaption, summary, details, section, article, main, aside, nav, footer, header');
        for (var bi = 0; bi < blockTags.length; bi++) {{
            blockTags[bi].style.fontWeight = 'normal';
        }}

        /* E3. Bold elements: explicitly bold */
        var boldTags = clone.querySelectorAll('strong, b');
        for (var bo = 0; bo < boldTags.length; bo++) {{
            boldTags[bo].style.fontWeight = 'bold';
        }}

        /* E4. Headings: bold + sized so Docs treats them as headings */
        var hSizeMap = {{'H1':'24px','H2':'20px','H3':'17px','H4':'14px','H5':'12px','H6':'11px'}};
        var headingTags = clone.querySelectorAll('h1, h2, h3, h4, h5, h6');
        for (var hi = 0; hi < headingTags.length; hi++) {{
            headingTags[hi].style.fontWeight = 'bold';
            headingTags[hi].style.fontSize = hSizeMap[headingTags[hi].tagName] || '14px';
        }}

        /* E5. Table headers: bold */
        var thTags = clone.querySelectorAll('th');
        for (var ti = 0; ti < thTags.length; ti++) {{
            thTags[ti].style.fontWeight = 'bold';
        }}

        /* E6. Italic elements: ensure they don't accidentally become bold */
        var emTags = clone.querySelectorAll('em, i');
        for (var ei = 0; ei < emTags.length; ei++) {{
            var emEl = emTags[ei];
            /* Only force normal if NOT inside a <strong>/<b> */
            var parentBold = emEl.closest('strong, b');
            if (!parentBold) {{
                emEl.style.fontWeight = 'normal';
            }}
            emEl.style.fontStyle = 'italic';
        }}

        /* E7. Code elements: monospace + normal weight */
        var codeTags = clone.querySelectorAll('code, pre');
        for (var ci = 0; ci < codeTags.length; ci++) {{
            codeTags[ci].style.fontFamily = '"Courier New", Courier, monospace';
            codeTags[ci].style.fontWeight = 'normal';
        }}

        /* E8. Links: normal weight + underline */
        var linkTags = clone.querySelectorAll('a');
        for (var li = 0; li < linkTags.length; li++) {{
            var linkEl = linkTags[li];
            var linkParentBold = linkEl.closest('strong, b');
            if (!linkParentBold) {{
                linkEl.style.fontWeight = 'normal';
            }}
        }}

        /* E9. Any stray <span> NOT inside <strong>/<b>/heading → normal */
        var spanTags = clone.querySelectorAll('span');
        for (var si = 0; si < spanTags.length; si++) {{
            var sp = spanTags[si];
            var spanParentBold = sp.closest('strong, b, h1, h2, h3, h4, h5, h6, th');
            if (!spanParentBold) {{
                sp.style.fontWeight = 'normal';
            }}
        }}

        return clone;
    }}

    async function copyRenderedContent() {{
        var btn = document.getElementById('copyBtn');
        var icon = document.getElementById('copyIcon');
        var text = document.getElementById('copyText');
        var status = document.getElementById('copyStatus');
        
        try {{
            var b64 = "{b64_html}";
            var htmlContent = b64DecodeUnicode(b64);
            
            var iframe = document.createElement('iframe');
            iframe.style.position = 'fixed';
            iframe.style.left = '-9999px';
            iframe.style.top = '-9999px';
            iframe.style.width = '800px';
            iframe.style.height = '600px';
            document.body.appendChild(iframe);
            
            iframe.contentDocument.open();
            iframe.contentDocument.write(htmlContent);
            iframe.contentDocument.close();
            
            await new Promise(function(resolve) {{ setTimeout(resolve, 2000); }});
            
            var contentDiv = iframe.contentDocument.getElementById('content');
            
            if (contentDiv) {{
                var cleanedContent = cleanForGoogleDocs(contentDiv);
                var renderedHTML = cleanedContent.innerHTML;
                var plainText = cleanedContent.innerText;
                
                try {{
                    var clipboardItem = new ClipboardItem({{
                        'text/html': new Blob([renderedHTML], {{ type: 'text/html' }}),
                        'text/plain': new Blob([plainText], {{ type: 'text/plain' }})
                    }});
                    await navigator.clipboard.write([clipboardItem]);
                    
                    icon.textContent = '✅';
                    text.textContent = 'Copied!';
                    status.textContent = 'Rich content copied — paste into Docs, Word, Outlook, etc.';
                    status.style.color = 'green';
                    status.style.opacity = '1';
                    btn.style.background = '#2e7d32';
                    
                }} catch (clipErr) {{
                    await navigator.clipboard.writeText(plainText);
                    icon.textContent = '📝';
                    text.textContent = 'Copied as Text';
                    status.textContent = 'Copied as plain text (browser blocked rich copy)';
                    status.style.color = '#b37000';
                    status.style.opacity = '1';
                    btn.style.background = '#b37000';
                }}
            }} else {{
                throw new Error('Content element not found');
            }}
            
            document.body.removeChild(iframe);
            
            setTimeout(function() {{
                icon.textContent = '📋';
                text.textContent = 'Copy Rendered Content';
                status.style.opacity = '0';
                btn.style.background = '#333';
            }}, 3000);
            
        }} catch (err) {{
            icon.textContent = '❌';
            text.textContent = 'Copy Failed';
            status.textContent = 'Error: ' + err.message;
            status.style.color = 'red';
            status.style.opacity = '1';
            btn.style.background = '#c62828';
            
            setTimeout(function() {{
                icon.textContent = '📋';
                text.textContent = 'Copy Rendered Content';
                status.style.opacity = '0';
                btn.style.background = '#333';
            }}, 3000);
        }}
    }}
    </script>
    """
    return copy_component


# ==========================================
# 7. USER INTERFACE
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
        [
            "PDF (Direct Download)",
            "PDF (Browser Print-Ready HTML)",
            "HTML (Rich Document)",
            "Plain Text (.txt)",
            "Markdown (.md)",
            "reStructuredText (.rst)",
            "LaTeX (.tex)"
        ],
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
    
    st.markdown("---")
    st.markdown("### 💡 PDF Tips")
    st.markdown(
        "**Direct Download** uses `fpdf2` or `reportlab` if installed.\n\n"
        "**Browser Print-Ready** opens an HTML file with a PDF save button — "
        "best for complex math/tables.\n\n"
        "Install for best results:\n"
        "```\npip install fpdf2\n```"
    )

# --- Initialize Session State ---
if 'raw_text' not in st.session_state:
    st.session_state.raw_text = ""
if 'rendered_text' not in st.session_state:
    st.session_state.rendered_text = ""
if 'is_rendered' not in st.session_state:
    st.session_state.is_rendered = False

# --- Callbacks ---
def on_render_click():
    st.session_state.raw_text = st.session_state.input_text_area
    if enable_latex_fix:
        st.session_state.rendered_text = preprocess_text(st.session_state.raw_text)
    else:
        st.session_state.rendered_text = st.session_state.raw_text
    st.session_state.is_rendered = True

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

else:
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
# 8. FOOTER: COPY, EXPORT & METRICS
# ==========================================
st.markdown("---")

if st.session_state.is_rendered and st.session_state.rendered_text.strip():
    
    # --- Copy Button ---
    st.subheader("📋 Copy Rendered Content")
    st.caption("Copies rich HTML to clipboard. Paste into Google Docs, Word, Outlook, etc. with formatting preserved.")
    st.components.v1.html(render_copy_button(st.session_state.rendered_text), height=60)
    
    st.markdown("---")
    
    # --- Export Section ---
    st.subheader("📦 Download Exported File")
    
    rendered = st.session_state.rendered_text
    raw = st.session_state.raw_text
    fname = export_filename.strip() if export_filename.strip() else "rendered_document"
    
    if export_format == "HTML (Rich Document)":
        file_content = generate_full_html(rendered, title=fname)
        file_bytes = file_content.encode('utf-8')
        file_ext = "html"
        mime = "text/html"
        description = "Self-contained HTML file with math, code highlighting, and clean styling. Opens in any browser. Includes a built-in Print/PDF button."
        
    elif export_format == "PDF (Direct Download)":
        pdf_bytes = generate_pdf_bytes(rendered, title=fname)
        if pdf_bytes is not None:
            file_bytes = pdf_bytes
            file_ext = "pdf"
            mime = "application/pdf"
            description = "PDF generated directly. For complex math/tables, consider the 'Browser Print-Ready HTML' option for best results."
        else:
            file_content = generate_pdf_via_js(rendered, title=fname)
            file_bytes = file_content.encode('utf-8')
            file_ext = "html"
            mime = "text/html"
            description = "⚠️ No PDF library found (`fpdf2` or `reportlab`). Downloading a Print-Ready HTML instead. Open it in your browser and click 'Download as PDF'. Install `fpdf2` with: `pip install fpdf2`"
        
    elif export_format == "PDF (Browser Print-Ready HTML)":
        file_content = generate_pdf_via_js(rendered, title=fname)
        file_bytes = file_content.encode('utf-8')
        file_ext = "html"
        mime = "text/html"
        description = "An HTML file with **html2pdf.js** built in. Open it in your browser → click '📥 Download as PDF' for a client-side PDF, or use '🖨️ Print → Save as PDF'. Best for complex math and tables."
        
    elif export_format == "Plain Text (.txt)":
        file_content = generate_txt(raw)
        file_bytes = file_content.encode('utf-8')
        file_ext = "txt"
        mime = "text/plain"
        description = "Plain text file with raw content as-is."
        
    elif export_format == "Markdown (.md)":
        file_content = generate_md(raw)
        file_bytes = file_content.encode('utf-8')
        file_ext = "md"
        mime = "text/markdown"
        description = "Markdown file for editors like VS Code, Typora, Obsidian, GitHub."
        
    elif export_format == "reStructuredText (.rst)":
        file_content = generate_rst(raw)
        file_bytes = file_content.encode('utf-8')
        file_ext = "rst"
        mime = "text/x-rst"
        description = "reStructuredText for Sphinx/Python documentation. Basic conversion from Markdown."
        
    elif export_format == "LaTeX (.tex)":
        file_content = generate_latex_doc(raw)
        file_bytes = file_content.encode('utf-8')
        file_ext = "tex"
        mime = "application/x-tex"
        description = "LaTeX document with preamble. Compile with pdflatex/xelatex/lualatex."
    
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
