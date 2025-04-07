from flask import Flask, request, send_file, jsonify
import os
import subprocess
import uuid
from flask_cors import CORS
import tempfile

app = Flask(__name__)
# Enable CORS for all domains with support for credentials
CORS(app, supports_credentials=True)

@app.route("/")
def home():
    return "Welcome to Rizzume - Resume Generator API!"

def escape_latex(text):
    """Escape LaTeX special characters"""
    if not text:
        return ""
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
        '^': r'\textasciicircum{}'
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text

def generate_pdf(latex_content):
    try:
        # Use tempfile for cross-platform compatibility
        with tempfile.TemporaryDirectory() as temp_dir:
            unique_id = str(uuid.uuid4())[:8]
            base_filename = f"resume_{unique_id}"
            tex_filename = f"{base_filename}.tex"
            pdf_filename = f"{base_filename}.pdf"

            tex_file_path = os.path.join(temp_dir, tex_filename)
            pdf_file_path = os.path.join(temp_dir, pdf_filename)

            # Write .tex file
            with open(tex_file_path, 'w', encoding='utf-8') as latex_file:
                latex_file.write(latex_content)

            # Save a debug copy
            debug_path = os.path.join(temp_dir, "debug_latest.tex")
            with open(debug_path, 'w', encoding='utf-8') as debug_file:
                debug_file.write(latex_content)

            original_dir = os.getcwd()
            os.chdir(temp_dir)

            try:
                # Run pdflatex command
                cmd = ["pdflatex", "-interaction=nonstopmode", tex_filename]
                result = subprocess.run(cmd, capture_output=True, text=True)

                # Log the output for debugging
                with open(os.path.join(temp_dir, "pdflatex_output.log"), "w") as log:
                    log.write(f"COMMAND: {' '.join(cmd)}\n\n")
                    log.write(f"STDOUT:\n{result.stdout}\n\n")
                    log.write(f"STDERR:\n{result.stderr}\n\n")
                    log.write(f"RETURN CODE: {result.returncode}\n")

                if os.path.exists(pdf_file_path):
                    # Return the full path to the generated PDF
                    return pdf_file_path
                else:
                    return None
            finally:
                os.chdir(original_dir)
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None

@app.route("/generate-pdf", methods=["POST"])
def generate_resume():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

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



        # Generate LaTeX content (same as your original code)
        # ... (your existing LaTeX generation code)

        # Make sure you include all the sections (education, experience, etc.)
        
        # After generating the PDF
        pdf_path = generate_pdf(latex_content)

        if pdf_path and os.path.exists(pdf_path):
            return send_file(pdf_path, 
                           mimetype='application/pdf',
                           as_attachment=True, 
                           download_name="resume.pdf")
        else:
            return jsonify({"error": "Failed to generate PDF"}), 500

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
