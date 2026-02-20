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
    .copy-success {
        color: #4CAF50;
        font-weight: bold;
        animation: fadeIn 0.3s ease-in;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-5px); }
        to { opacity: 1; transform: translateY(0); }
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
# 4. EXPORT FUNCTIONALITY - MULTIPLE FORMATS
# ==========================================

def generate_rich_html(raw_text, title="Exported Document"):
    """Generates a fully self-contained HTML document with KaTeX, syntax highlighting, and styling."""
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    
    <!-- KaTeX for Math Rendering -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"
        onload="renderMathInElement(document.body, {{
            delimiters: [
                {{left: '$$', right: '$$', display: true}},
                {{left: '$', right: '$', display: false}},
                {{left: '\\\\(', right: '\\\\)', display: false}},
                {{left: '\\\\[', right: '\\\\]', display: true}}
            ]
        }});"></script>
    
    <!-- Marked.js for Markdown Rendering -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    
    <!-- Highlight.js for Code Syntax Highlighting -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/github.min.css">
    <script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js"></script>
    
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            line-height: 1.8;
            color: #333;
            background-color: #fafafa;
        }}
        h1 {{ font-size: 2em; margin: 20px 0 10px; color: #1a1a2e; border-bottom: 2px solid #009879; padding-bottom: 5px; }}
        h2 {{ font-size: 1.6em; margin: 18px 0 8px; color: #16213e; }}
        h3 {{ font-size: 1.3em; margin: 15px 0 8px; color: #0f3460; }}
        h4, h5, h6 {{ margin: 12px 0 6px; color: #444; }}
        p {{ margin: 10px 0; }}
        a {{ color: #009879; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        blockquote {{
            border-left: 4px solid #009879;
            padding: 10px 20px;
            margin: 15px 0;
            background-color: #f0f7f4;
            color: #555;
            font-style: italic;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 10px 14px;
            text-align: left;
        }}
        th {{
            background-color: #009879;
            color: #fff;
        }}
        tbody tr:nth-child(even) {{ background-color: #f2f2f2; }}
        tbody tr:hover {{ background-color: #e8f5e9; }}
        pre {{
            background-color: #282c34;
            color: #abb2bf;
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 15px 0;
            font-size: 0.9em;
        }}
        code {{
            font-family: 'Fira Code', 'Courier New', monospace;
        }}
        :not(pre) > code {{
            background-color: #e8e8e8;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.9em;
            color: #c7254e;
        }}
        ul, ol {{ margin: 10px 0 10px 25px; }}
        li {{ margin: 4px 0; }}
        hr {{ border: none; border-top: 2px solid #ddd; margin: 25px 0; }}
        img {{ max-width: 100%; height: auto; border-radius: 8px; margin: 10px 0; }}
        .katex-display {{ overflow-x: auto; padding: 10px 0; }}
        .footer {{
            margin-top: 40px;
            padding-top: 15px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #999;
            font-size: 0.85em;
        }}
    </style>
</head>
<body>
    <div id="content">{raw_text}</div>
    
    <div class="footer">
        Generated by Advanced Universal Renderer
    </div>
    
    <script>
        // Parse Markdown content
        const contentEl = document.getElementById('content');
        const rawText = contentEl.innerHTML;
        
        // Configure marked
        marked.setOptions({{
            gfm: true,
            breaks: true,
            highlight: function(code, lang) {{
                if (lang && hljs.getLanguage(lang)) {{
                    return hljs.highlight(code, {{ language: lang }}).value;
                }}
                return hljs.highlightAuto(code).value;
            }}
        }});
        
        contentEl.innerHTML = marked.parse(rawText);
        
        // Apply syntax highlighting to any remaining code blocks
        document.querySelectorAll('pre code').forEach((block) => {{
            hljs.highlightBlock(block);
        }});
    </script>
</body>
</html>"""
    return html_content


def generate_rich_html_for_copy(raw_text):
    """
    Generates a rich HTML snippet for clipboard copying.
    When pasted into rich-text editors (Gmail, Google Docs, Word, etc.),
    it preserves formatting including math rendered as images.
    """
    # Convert markdown-style formatting to HTML
    processed = raw_text
    
    # Convert headers
    processed = re.sub(r'^######\s+(.+)$', r'<h6>\1</h6>', processed, flags=re.MULTILINE)
    processed = re.sub(r'^#####\s+(.+)$', r'<h5>\1</h5>', processed, flags=re.MULTILINE)
    processed = re.sub(r'^####\s+(.+)$', r'<h4>\1</h4>', processed, flags=re.MULTILINE)
    processed = re.sub(r'^###\s+(.+)$', r'<h3>\1</h3>', processed, flags=re.MULTILINE)
    processed = re.sub(r'^##\s+(.+)$', r'<h2>\1</h2>', processed, flags=re.MULTILINE)
    processed = re.sub(r'^#\s+(.+)$', r'<h1>\1</h1>', processed, flags=re.MULTILINE)
    
    # Convert bold and italic
    processed = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', processed)
    processed = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', processed)
    processed = re.sub(r'\*(.+?)\*', r'<em>\1</em>', processed)
    
    # Convert inline code
    processed = re.sub(r'`([^`]+)`', r'<code style="background-color:#f0f0f0;padding:2px 6px;border-radius:3px;font-family:monospace;color:#c7254e;">\1</code>', processed)
    
    # Convert code blocks
    def replace_code_block(match):
        lang = match.group(1) or ""
        code = match.group(2)
        return f'<pre style="background-color:#282c34;color:#abb2bf;padding:16px;border-radius:8px;overflow-x:auto;font-family:monospace;"><code>{code}</code></pre>'
    processed = re.sub(r'```(\w*)\n(.*?)```', replace_code_block, processed, flags=re.DOTALL)
    
    # Convert block math $$ ... $$ to rendered image via codecogs API
    def replace_block_math(match):
        math_content = match.group(1).strip()
        encoded_math = base64.b64encode(math_content.encode()).decode()
        # Use an online LaTeX rendering service for the copy
        from urllib.parse import quote
        latex_url = f"https://latex.codecogs.com/png.latex?\\dpi{{150}}\\bg_white {quote(math_content)}"
        return f'<div style="text-align:center;margin:15px 0;"><img src="{latex_url}" alt="{math_content}" style="max-width:100%;"/></div>'
    processed = re.sub(r'\$\$(.*?)\$\$', replace_block_math, processed, flags=re.DOTALL)
    
    # Convert inline math $ ... $ to rendered image
    def replace_inline_math(match):
        math_content = match.group(1).strip()
        from urllib.parse import quote
        latex_url = f"https://latex.codecogs.com/png.latex?\\dpi{{110}} {quote(math_content)}"
        return f'<img src="{latex_url}" alt="{math_content}" style="vertical-align:middle;"/>'
    processed = re.sub(r'(?<!\$)\$(?!\$)(.+?)\$(?!\$)', replace_inline_math, processed)
    
    # Convert blockquotes
    processed = re.sub(r'^>\s+(.+)$', r'<blockquote style="border-left:4px solid #009879;padding:10px 20px;margin:10px 0;background-color:#f0f7f4;color:#555;font-style:italic;">\1</blockquote>', processed, flags=re.MULTILINE)
    
    # Convert horizontal rules
    processed = re.sub(r'^---+$', r'<hr style="border:none;border-top:2px solid #ddd;margin:20px 0;">', processed, flags=re.MULTILINE)
    
    # Convert unordered lists
    processed = re.sub(r'^\-\s+(.+)$', r'<li>\1</li>', processed, flags=re.MULTILINE)
    processed = re.sub(r'((?:<li>.*?</li>\n?)+)', r'<ul style="margin:10px 0 10px 25px;">\1</ul>', processed)
    
    # Convert line breaks (remaining plain lines)
    lines = processed.split('\n')
    result_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('<'):
            result_lines.append(f'<p style="margin:8px 0;line-height:1.6;">{stripped}</p>')
        else:
            result_lines.append(line)
    processed = '\n'.join(result_lines)
    
    # Convert markdown tables to HTML tables
    def convert_table(text):
        lines = text.split('\n')
        result = []
        table_lines = []
        in_table = False
        
        for line in lines:
            stripped = line.strip()
            if '|' in stripped and not stripped.startswith('<'):
                # Check if it's a table separator line
                if re.match(r'^[\|\s\-:]+$', stripped):
                    in_table = True
                    continue
                table_lines.append(stripped)
                in_table = True
            else:
                if table_lines:
                    # Build HTML table
                    table_html = '<table style="width:100%;border-collapse:collapse;margin:15px 0;box-shadow:0 0 10px rgba(0,0,0,0.1);">'
                    for i, tl in enumerate(table_lines):
                        cells = [c.strip() for c in tl.strip('|').split('|')]
                        if i == 0:
                            table_html += '<thead><tr>'
                            for cell in cells:
                                table_html += f'<th style="background-color:#009879;color:#fff;padding:10px 14px;border:1px solid #ddd;">{cell}</th>'
                            table_html += '</tr></thead><tbody>'
                        else:
                            bg = '#f9f9f9' if i % 2 == 0 else '#ffffff'
                            table_html += f'<tr style="background-color:{bg};">'
                            for cell in cells:
                                table_html += f'<td style="padding:10px 14px;border:1px solid #ddd;">{cell}</td>'
                            table_html += '</tr>'
                    table_html += '</tbody></table>'
                    result.append(table_html)
                    table_lines = []
                in_table = False
                result.append(line)
        
        # Handle table at end of text
        if table_lines:
            table_html = '<table style="width:100%;border-collapse:collapse;margin:15px 0;">'
            for i, tl in enumerate(table_lines):
                cells = [c.strip() for c in tl.strip('|').split('|')]
                if i == 0:
                    table_html += '<thead><tr>'
                    for cell in cells:
                        table_html += f'<th style="background-color:#009879;color:#fff;padding:10px 14px;border:1px solid #ddd;">{cell}</th>'
                    table_html += '</tr></thead><tbody>'
                else:
                    bg = '#f9f9f9' if i % 2 == 0 else '#ffffff'
                    table_html += f'<tr style="background-color:{bg};">'
                    for cell in cells:
                        table_html += f'<td style="padding:10px 14px;border:1px solid #ddd;">{cell}</td>'
                    table_html += '</tr>'
            table_html += '</tbody></table>'
            result.append(table_html)
        
        return '\n'.join(result)
    
    processed = convert_table(processed)
    
    # Wrap in a styled container
    full_html = f"""<div style="font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;max-width:800px;line-height:1.8;color:#333;">
{processed}
</div>"""
    
    return full_html


def generate_txt(raw_text):
    """Generates plain text by stripping markdown/LaTeX syntax."""
    text = raw_text
    # Remove markdown headers
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    # Remove bold/italic markers
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\1', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    # Remove inline code backticks
    text = re.sub(r'`([^`]+)`', r'\1', text)
    # Remove code block markers
    text = re.sub(r'```\w*\n', '', text)
    text = re.sub(r'```', '', text)
    # Remove $$ math delimiters but keep content
    text = re.sub(r'\$\$', '', text)
    text = re.sub(r'\$', '', text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove image markdown
    text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', r'\1', text)
    # Remove link markdown, keep text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Clean up extra whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def generate_pdf_html(raw_text):
    """
    Generates an HTML page designed for PDF printing via the browser.
    Includes a print button and auto-print script.
    """
    base_html = generate_rich_html(raw_text, title="Document Export")
    # Inject print-specific styles and auto-print
    print_additions = """
    <style>
        @media print {
            .no-print { display: none !important; }
            body { padding: 0; margin: 20px; }
        }
    </style>
    <div class="no-print" style="text-align:center;margin-bottom:20px;padding:15px;background:#fff3cd;border:1px solid #ffc107;border-radius:8px;">
        <p style="margin:0 0 10px 0;font-size:1.1em;"><strong>📄 To save as PDF:</strong></p>
        <p style="margin:0 0 15px 0;">Click the button below, then choose <strong>"Save as PDF"</strong> as the destination in the print dialog.</p>
        <button onclick="window.print()" style="padding:12px 30px;font-size:1.1em;background-color:#009879;color:white;border:none;border-radius:8px;cursor:pointer;font-weight:bold;">
            🖨️ Print / Save as PDF
        </button>
    </div>
    """
    # Insert after <body>
    pdf_html = base_html.replace('<body>', f'<body>\n{print_additions}', 1)
    return pdf_html


def generate_markdown_file(raw_text):
    """Returns the raw markdown text for .md download."""
    return raw_text


def generate_rst(raw_text):
    """Basic Markdown to reStructuredText conversion."""
    text = raw_text
    
    # Convert headers
    lines = text.split('\n')
    result = []
    for line in lines:
        h_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if h_match:
            level = len(h_match.group(1))
            title = h_match.group(2)
            chars = {1: '=', 2: '-', 3: '~', 4: '^', 5: '"', 6: "'"}
            underline = chars.get(level, '-') * len(title)
            if level == 1:
                result.append(underline)
                result.append(title)
                result.append(underline)
            else:
                result.append(title)
                result.append(underline)
        else:
            result.append(line)
    
    text = '\n'.join(result)
    
    # Convert bold
    text = re.sub(r'\*\*(.+?)\*\*', r'**\1**', text)
    # Convert italic
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)\*(?!\*)', r'*\1*', text)
    # Convert inline code
    text = re.sub(r'`([^`]+)`', r'``\1``', text)
    
    return text


def generate_latex_doc(raw_text):
    """Converts markdown-style text into a LaTeX document."""
    text = raw_text
    
    preamble = r"""\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{booktabs}
\usepackage{geometry}
\geometry{margin=1in}

\lstset{
    basicstyle=\ttfamily\small,
    backgroundcolor=\color{gray!10},
    frame=single,
    breaklines=true,
    numbers=left,
    numberstyle=\tiny\color{gray},
}

\begin{document}

"""
    
    postamble = r"""
\end{document}"""
    
    # Convert headers
    text = re.sub(r'^#\s+(.+)$', r'\\section{\1}', text, flags=re.MULTILINE)
    text = re.sub(r'^##\s+(.+)$', r'\\subsection{\1}', text, flags=re.MULTILINE)
    text = re.sub(r'^###\s+(.+)$', r'\\subsubsection{\1}', text, flags=re.MULTILINE)
    text = re.sub(r'^####\s+(.+)$', r'\\paragraph{\1}', text, flags=re.MULTILINE)
    
    # Convert bold and italic
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\\textbf{\\textit{\1}}', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)\*(?!\*)', r'\\textit{\1}', text)
    
    # Convert inline code
    text = re.sub(r'`([^`]+)`', r'\\texttt{\1}', text)
    
    # Convert code blocks
    def replace_code_latex(match):
        lang = match.group(1) or ""
        code = match.group(2)
        if lang:
            return f'\\begin{{lstlisting}}[language={lang}]\n{code}\\end{{lstlisting}}'
        return f'\\begin{{lstlisting}}\n{code}\\end{{lstlisting}}'
    text = re.sub(r'```(\w*)\n(.*?)```', replace_code_latex, text, flags=re.DOTALL)
    
    # Convert blockquotes
    text = re.sub(r'^>\s+(.+)$', r'\\begin{quote}\1\\end{quote}', text, flags=re.MULTILINE)
    
    # Convert horizontal rules
    text = re.sub(r'^---+$', r'\\hrulefill', text, flags=re.MULTILINE)
    
    # Convert unordered lists
    text = re.sub(r'^\-\s+(.+)$', r'\\item \1', text, flags=re.MULTILINE)
    
    return preamble + text + postamble


# ==========================================
# 5. COPY TO CLIPBOARD FUNCTIONALITY
# ==========================================
def create_copy_button(text_to_copy, rendered_html):
    """
    Creates a copy button that copies rich HTML to clipboard.
    When pasted, it preserves formatting in rich-text editors.
    """
    # Escape for JavaScript
    escaped_html = rendered_html.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
    escaped_plain = text_to_copy.replace('\\', '\\\\').replace('`', '\\`').replace("'", "\\'").replace('\n', '\\n')
    
    copy_button_html = f"""
    <div style="margin: 10px 0;">
        <button id="copyBtn" onclick="copyRichText()" style="
            padding: 10px 20px;
            background-color: #2196F3;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            font-weight: bold;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s ease;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        "
        onmouseover="this.style.backgroundColor='#1976D2';this.style.transform='translateY(-1px)';this.style.boxShadow='0 4px 8px rgba(0,0,0,0.3)';"
        onmouseout="this.style.backgroundColor='#2196F3';this.style.transform='translateY(0)';this.style.boxShadow='0 2px 5px rgba(0,0,0,0.2)';">
            📋 Copy Rendered Text
        </button>
        <span id="copyStatus" style="margin-left: 10px; display: none; color: #4CAF50; font-weight: bold;">
            ✅ Copied! Paste into any rich-text editor.
        </span>
    </div>
    
    <script>
    async function copyRichText() {{
        const htmlContent = `{escaped_html}`;
        const plainText = `{escaped_plain}`;
        
        try {{
            // Use Clipboard API with HTML mime type for rich text
            const blobHtml = new Blob([htmlContent], {{ type: 'text/html' }});
            const blobText = new Blob([plainText], {{ type: 'text/plain' }});
            
            const clipboardItem = new ClipboardItem({{
                'text/html': blobHtml,
                'text/plain': blobText
            }});
            
            await navigator.clipboard.write([clipboardItem]);
            
            // Show success
            const btn = document.getElementById('copyBtn');
            const status = document.getElementById('copyStatus');
            btn.innerHTML = '✅ Copied!';
            btn.style.backgroundColor = '#4CAF50';
            status.style.display = 'inline';
            
            setTimeout(() => {{
                btn.innerHTML = '📋 Copy Rendered Text';
                btn.style.backgroundColor = '#2196F3';
                status.style.display = 'none';
            }}, 3000);
            
        }} catch (err) {{
            // Fallback: copy as plain text
            try {{
                await navigator.clipboard.writeText(plainText);
                const btn = document.getElementById('copyBtn');
                btn.innerHTML = '✅ Copied (plain text)';
                btn.style.backgroundColor = '#FF9800';
                setTimeout(() => {{
                    btn.innerHTML = '📋 Copy Rendered Text';
                    btn.style.backgroundColor = '#2196F3';
                }}, 3000);
            }} catch (e) {{
                // Last resort fallback
                const textarea = document.createElement('textarea');
                textarea.value = plainText;
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                
                const btn = document.getElementById('copyBtn');
                btn.innerHTML = '✅ Copied (plain text)';
                btn.style.backgroundColor = '#FF9800';
                setTimeout(() => {{
                    btn.innerHTML = '📋 Copy Rendered Text';
                    btn.style.backgroundColor = '#2196F3';
                }}, 3000);
            }}
        }}
    }}
    </script>
    """
    return copy_button_html


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
        "Select Export Format",
        ["HTML (Rich Document)", "PDF (Print-Ready)", "Plain Text (.txt)", "Markdown (.md)", "LaTeX (.tex)", "reStructuredText (.rst)"],
        index=0
    )
    
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
    st.markdown("### Export Formats:")
    st.markdown(
        "- 📄 **HTML**: Fully styled, self-contained\n"
        "- 🖨️ **PDF**: Print-ready with print dialog\n"
        "- 📝 **TXT**: Plain text, no formatting\n"
        "- 📋 **MD**: Raw Markdown preserved\n"
        "- 📐 **TEX**: LaTeX document format\n"
        "- 📑 **RST**: reStructuredText format"
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
# 7. FOOTER: COPY BUTTON, EXPORT & METRICS
# ==========================================
st.markdown("---")

if st.session_state.is_rendered and st.session_state.rendered_text.strip():
    
    # --- Copy Button Section ---
    st.subheader("📋 Copy & Export")
    
    # Generate rich HTML for copying
    rich_html_for_copy = generate_rich_html_for_copy(st.session_state.rendered_text)
    copy_btn_html = create_copy_button(st.session_state.rendered_text, rich_html_for_copy)
    st.markdown(copy_btn_html, unsafe_allow_html=True)
    
    st.caption("💡 **Tip:** The copied text will paste as formatted content in Gmail, Google Docs, Microsoft Word, Notion, and other rich-text editors.")
    
    st.markdown("---")
    
    # --- Export Section ---
    st.subheader("📥 Download")
    
    exp_col1, exp_col2 = st.columns([2, 3])
    
    with exp_col1:
        st.markdown(f"**Selected format:** `{export_format}`")
        
        # Generate the appropriate file based on selection
        if export_format == "HTML (Rich Document)":
            file_content = generate_rich_html(st.session_state.rendered_text)
            file_name = "rendered_document.html"
            mime_type = "text/html"
            file_bytes = file_content.encode('utf-8')
            
        elif export_format == "PDF (Print-Ready)":
            file_content = generate_pdf_html(st.session_state.rendered_text)
            file_name = "rendered_document_print.html"
            mime_type = "text/html"
            file_bytes = file_content.encode('utf-8')
            
        elif export_format == "Plain Text (.txt)":
            file_content = generate_txt(st.session_state.raw_text)
            file_name = "rendered_document.txt"
            mime_type = "text/plain"
            file_bytes = file_content.encode('utf-8')
            
        elif export_format == "Markdown (.md)":
            file_content = generate_markdown_file(st.session_state.raw_text)
            file_name = "rendered_document.md"
            mime_type = "text/markdown"
            file_bytes = file_content.encode('utf-8')
            
        elif export_format == "LaTeX (.tex)":
            file_content = generate_latex_doc(st.session_state.raw_text)
            file_name = "rendered_document.tex"
            mime_type = "application/x-tex"
            file_bytes = file_content.encode('utf-8')
            
        elif export_format == "reStructuredText (.rst)":
            file_content = generate_rst(st.session_state.raw_text)
            file_name = "rendered_document.rst"
            mime_type = "text/x-rst"
            file_bytes = file_content.encode('utf-8')
        
        st.download_button(
            label=f"📥 Download as {file_name.split('.')[-1].upper()}",
            data=file_bytes,
            file_name=file_name,
            mime=mime_type,
            use_container_width=True,
            type="primary"
        )
        
        if export_format == "PDF (Print-Ready)":
            st.info("📌 **PDF Export:** The downloaded HTML file will open in your browser with a **Print** button. Use **'Save as PDF'** in the print dialog to create your PDF.")
    
    with exp_col2:
        # Preview of what will be exported
        with st.expander("👁️ Preview Export Content", expanded=False):
            if export_format in ["Plain Text (.txt)", "Markdown (.md)", "LaTeX (.tex)", "reStructuredText (.rst)"]:
                st.code(file_content, language="text" if export_format == "Plain Text (.txt)" else 
                        "markdown" if export_format == "Markdown (.md)" else
                        "latex" if export_format == "LaTeX (.tex)" else "rst")
            else:
                st.markdown("*HTML preview not shown here. Download to view in browser.*")
                st.code(file_content[:2000] + "\n\n... (truncated)" if len(file_content) > 2000 else file_content, language="html")
    
    st.markdown("---")
    
    # --- Metrics Section ---
    st.subheader("📊 Document Statistics")
    words = len(st.session_state.raw_text.split())
    chars = len(st.session_state.raw_text)
    lines = len(st.session_state.raw_text.split('\n'))
    
    # Count specific elements
    headers = len(re.findall(r'^#{1,6}\s', st.session_state.raw_text, re.MULTILINE))
    code_blocks = len(re.findall(r'```', st.session_state.raw_text)) // 2
    math_blocks = len(re.findall(r'\$\$', st.session_state.rendered_text)) // 2
    inline_math = len(re.findall(r'(?<!\$)\$(?!\$)(.+?)\$(?!\$)', st.session_state.rendered_text))
    
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("📝 Words", words)
    m2.metric("🔤 Characters", chars)
    m3.metric("📄 Lines", lines)
    m4.metric("📌 Headers", headers)
    m5.metric("💻 Code Blocks", code_blocks)
    m6.metric("📐 Math Expressions", math_blocks + inline_math)
