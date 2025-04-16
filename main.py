from flask import Flask, request, send_file, jsonify
import os
import subprocess
import uuid
import tempfile
import traceback
import sys
import logging
import shutil
from io import BytesIO
from flask_cors import CORS
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(process)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('rizzume')
logger.setLevel(logging.DEBUG)

# File handler for persistent logs
file_handler = logging.FileHandler('rizzume.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

app = Flask(__name__)
CORS(app)  # Allow all domains

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit
if os.name == 'nt':  # Windows
    TEMP_PDF_DIR = os.environ.get('TEMP_PDF_DIR', os.path.join(os.path.dirname(__file__), 'tmp', 'pdfs'))
else:  # Unix/Linux
    TEMP_PDF_DIR = os.environ.get('TEMP_PDF_DIR', '/tmp/pdfs')

def setup_environment():
    """Ensure required directories exist"""
    os.makedirs(TEMP_PDF_DIR, exist_ok=True)
    logger.info(f"Environment setup complete. Temp PDF dir: {TEMP_PDF_DIR}")
    logger.info(f"LaTeX version: {get_latex_version()}")

def get_latex_version():
    """Get installed LaTeX version"""
    try:
        result = subprocess.run(['pdflatex', '--version'], capture_output=True, text=True)
        return result.stdout.split('\n')[0] if result.returncode == 0 else "Not available"
    except Exception as e:
        logger.error(f"Error getting LaTeX version: {str(e)}")
        return "Error"

def escape_latex(text):
    """Enhanced LaTeX escaping with logging"""
    if not text:
        return ""
    
    original_text = text
    replacements = {
        '\\': r'\\textbackslash{}',
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}'
    }
    
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    
    if original_text != text:
        logger.debug(f"Escaped LaTeX special chars in: {original_text[:50]}...")
    
    return text

def generate_pdf(latex_content):
    """Generate PDF from LaTeX content with robust error handling"""
    temp_dir = None
    try:
        # Create a dedicated temp directory
        temp_dir = tempfile.mkdtemp(dir=TEMP_PDF_DIR)
        logger.info(f"Created temp directory: {temp_dir}")
        logger.debug(f"Directory writable: {os.access(temp_dir, os.W_OK)}")
        
        # Generate unique filenames
        unique_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"resume_{timestamp}_{unique_id}"
        tex_filename = f"{base_filename}.tex"
        pdf_filename = f"{base_filename}.pdf"
        
        tex_path = os.path.join(temp_dir, tex_filename)
        pdf_path = os.path.join(temp_dir, pdf_filename)
        
        # Write LaTeX content
        logger.info(f"Writing LaTeX to {tex_path}")
        with open(tex_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        # Save debug copy
        debug_path = os.path.join(temp_dir, "debug.tex")
        with open(debug_path, 'w') as f:
            f.write(latex_content)
        
        # Compile LaTeX
        current_dir = os.getcwd()
        os.chdir(temp_dir)
        logger.info(f"Changed to directory: {temp_dir}")
        
        cmd = [
            'pdflatex',
            '-interaction=nonstopmode',
            '-halt-on-error',
            '-file-line-error',
            tex_filename
        ]
        
        logger.info(f"Executing: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30  # 30 seconds timeout
        )
        
        # Save compilation logs
        with open(os.path.join(temp_dir, 'compile.log'), 'w') as f:
            f.write(f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}")
        
        logger.info(f"pdflatex return code: {result.returncode}")
        logger.debug(f"STDOUT: {result.stdout[:200]}...")
        logger.debug(f"STDERR: {result.stderr[:200]}...")
        
        # Check output
        if result.returncode != 0:
            logger.error(f"pdflatex failed with code {result.returncode}")
            if os.path.exists(f"{base_filename}.log"):
                with open(f"{base_filename}.log", 'r') as f:
                    logger.error(f"LaTeX log:\n{f.read()}")
            return None
        
        if not os.path.exists(pdf_path):
            logger.error("PDF file not generated")
            return None
        
        # Verify PDF is valid
        if os.path.getsize(pdf_path) < 100:  # At least 100 bytes
            logger.error("Generated PDF is too small (likely invalid)")
            return None
        
        # Read PDF content
        with open(pdf_path, 'rb') as f:
            pdf_content = f.read()
        
        logger.info(f"PDF generated successfully. Size: {len(pdf_content)} bytes")
        return pdf_content
        
    except subprocess.TimeoutExpired:
        logger.error("LaTeX compilation timed out after 30 seconds")
        return None
    except Exception as e:
        logger.error(f"Error in generate_pdf: {str(e)}")
        logger.error(traceback.format_exc())
        return None
    finally:
        try:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                logger.info(f"Cleaned up temp directory: {temp_dir}")
        except Exception as e:
            logger.error(f"Error cleaning up temp directory: {str(e)}")
        
        if 'current_dir' in locals():
            os.chdir(current_dir)

@app.route("/health")
def health_check():
    """Enhanced health check with system diagnostics"""
    health_data = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "system": {
            "latex": get_latex_version(),
            "python": sys.version,
            "disk_space": shutil.disk_usage("/").free,
            "temp_dir_writable": os.access(TEMP_PDF_DIR, os.W_OK)
        }
    }
    
    # Test PDF generation
    try:
        test_content = r"""\documentclass{article}\begin{document}Test PDF\end{document}"""
        pdf = generate_pdf(test_content)
        health_data["test_pdf"] = "success" if pdf else "failed"
    except Exception as e:
        health_data["test_pdf"] = f"error: {str(e)}"
    
    return jsonify(health_data)

@app.route("/generate-pdf", methods=["POST"])
def generate_resume():
    """Main PDF generation endpoint with detailed logging"""
    start_time = datetime.now()
    logger.info("PDF generation request started")
    
    try:
        # Validate input
        if not request.is_json:
            logger.error("Request is not JSON")
            return jsonify({"error": "Request must be JSON"}), 400
            
        data = request.get_json()
        logger.info(f"Request data keys: {list(data.keys())}")
        
        # [Rest of your existing resume generation code...]
        # (Keep all your existing LaTeX template generation code here)
         # Basic Info
        name = escape_latex(data.get("name", "Your Name"))
        phone = escape_latex(data.get("phone", "123-456-7890"))
        email = escape_latex(data.get("email", "example@email.com"))
        linkedin = escape_latex(data.get("linkedin", ""))
        github = escape_latex(data.get("github", ""))

        # Education
        education_latex = ""
        for edu in data.get("education", []):
            institution = escape_latex(edu.get("institution", ""))
            location = escape_latex(edu.get("location", ""))
            degree = escape_latex(edu.get("degree", ""))
            dates = escape_latex(edu.get("dates", ""))
            education_latex += f"""
    \\resumeSubheading
      {{{institution}}}{{{location}}}
      {{{degree}}}{{{dates}}}"""

        # Experience
        experience_latex = ""
        for exp in data.get("experience", []):
            position = escape_latex(exp.get("position", ""))
            dates = escape_latex(exp.get("dates", ""))
            company = escape_latex(exp.get("company", ""))
            location = escape_latex(exp.get("location", ""))

            experience_latex += f"""
    \\resumeSubheading
      {{{position}}}{{{dates}}}
      {{{company}}}{{{location}}}
      \\resumeItemListStart"""

            for bullet in exp.get("bullets", []):
                bullet_text = escape_latex(bullet)
                experience_latex += f"""
        \\resumeItem{{{bullet_text}}}"""

            experience_latex += """
      \\resumeItemListEnd"""

        # Projects
        projects_latex = ""
        for proj in data.get("projects", []):
            proj_name = escape_latex(proj.get("name", ""))
            technologies = escape_latex(proj.get("technologies", ""))
            dates = escape_latex(proj.get("dates", ""))

            projects_latex += f"""
    \\resumeProjectHeading
      {{\\textbf{{{proj_name}}} $|$ \\emph{{{technologies}}}}}{{{dates}}}
      \\resumeItemListStart"""

            for bullet in proj.get("bullets", []):
                bullet_text = escape_latex(bullet)
                projects_latex += f"""
        \\resumeItem{{{bullet_text}}}"""

            projects_latex += """
      \\resumeItemListEnd"""

        # Skills
        skills_latex = ""
        for category, items in data.get("skills", {}).items():
            category_text = escape_latex(category)
            skills_list = [escape_latex(skill) for skill in items]
            skills_text = ", ".join(skills_list)
            skills_latex += f"     \\textbf{{{category_text}}}: {skills_text} \\\\\n"

        # Final LaTeX document
        latex_content = r"""
\documentclass[letterpaper,11pt]{article}
\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}

\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}
\urlstyle{same}
\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

\titleformat{\section}{\vspace{-4pt}\scshape\raggedright\large}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]
\newcommand{\resumeItem}[1]{\item\small{{#1 \vspace{-2pt}}}}
\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}
\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & #2 \\
    \end{tabular*}\vspace{-7pt}
}
\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}
\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]} 
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}} 
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

\begin{document}
\begin{center}
    \textbf{\Huge \scshape """ + name + r"""} \\ \vspace{1pt}
    \small """ + phone + " $|$ \\href{mailto:" + email + "}{\\underline{" + email + "}} $|$ " + \
    "\\href{https://linkedin.com/in/" + linkedin + "}{\\underline{linkedin.com/in/" + linkedin + "}} $|$ " + \
    "\\href{https://github.com/" + github + "}{\\underline{github.com/" + github + "}}" + r"""
\end{center}

\section{Education}
\resumeSubHeadingListStart""" + education_latex + r"""
\resumeSubHeadingListEnd

\section{Experience}
\resumeSubHeadingListStart""" + experience_latex + r"""
\resumeSubHeadingListEnd

\section{Projects}
\resumeSubHeadingListStart""" + projects_latex + r"""
\resumeSubHeadingListEnd

\section{Technical Skills}
\begin{itemize}[leftmargin=0.15in, label={}]
    \small{\item{
""" + skills_latex + r"""
    }}
\end{itemize}
\end{document}
"""
        
        # Generate PDF
        logger.info("Starting PDF generation")
        pdf_content = generate_pdf(latex_content)
        
        if not pdf_content:
            logger.error("PDF generation failed")
            return jsonify({"error": "PDF generation failed"}), 500
        
        # Prepare response
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"Request completed in {duration:.2f} seconds")
        
        return send_file(
            BytesIO(pdf_content),
            as_attachment=True,
            download_name=f"resume_{datetime.now().strftime('%Y%m%d')}.pdf",
            mimetype="application/pdf"
        )
        
    except Exception as e:
        logger.error(f"Error in generate_resume: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "error": "Internal server error",
            "details": str(e),
            "traceback": traceback.format_exc()
        }), 500

# Initialize environment when starting
setup_environment()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting Rizzume API on port {port}")
    logger.info(f"Temp PDF directory: {TEMP_PDF_DIR}")
    app.run(host="0.0.0.0", port=port, debug=False)
