from flask import Flask, request, send_file, jsonify
import os
import subprocess
import uuid

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to Rizzume - Resume Generator API!"

def generate_pdf(latex_content):
    try:
        # Define the correct directory for PDF generation
        pdf_directory = "D:/Downloads/Projects/vs code/Rizzume"
        
        # Ensure the directory exists
        if not os.path.exists(pdf_directory):
            os.makedirs(pdf_directory)
        
        # Use a random filename to avoid conflicts
        unique_id = str(uuid.uuid4())[:8]
        base_filename = f"resume_{unique_id}"
        
        # Define the temporary file paths
        tex_file_path = os.path.join(pdf_directory, f"{base_filename}.tex")
        
        # Write the LaTeX content to the .tex file
        with open(tex_file_path, 'w', encoding='utf-8') as latex_file:
            latex_file.write(latex_content)
        
        # For convenience, save a copy with a fixed name for debugging
        debug_path = os.path.join(pdf_directory, "debug_latest.tex")
        with open(debug_path, 'w', encoding='utf-8') as debug_file:
            debug_file.write(latex_content)
        
        # Change to the output directory before running pdflatex
        original_dir = os.getcwd()
        os.chdir(pdf_directory)
        
        try:
            # Run pdflatex with simplified options
            cmd = ["pdflatex", "-interaction=nonstopmode", tex_file_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Log the full output for better debugging
            with open(os.path.join(pdf_directory, "pdflatex_output.log"), "w") as log:
                log.write(f"COMMAND: {' '.join(cmd)}\n\n")
                log.write(f"STDOUT:\n{result.stdout}\n\n")
                log.write(f"STDERR:\n{result.stderr}\n\n")
                log.write(f"RETURN CODE: {result.returncode}\n")
            
            # Check if PDF was generated (look for filename without .tex extension)
            pdf_file_path = os.path.join(pdf_directory, f"{base_filename}.pdf")
            if os.path.exists(pdf_file_path):
                print(f"PDF generated successfully at: {pdf_file_path}")
                return pdf_file_path
            else:
                print("PDF generation failed!")
                return None
                
        finally:
            # Change back to the original directory
            os.chdir(original_dir)
            
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None

def escape_latex(text):
    """Escape LaTeX special characters"""
    if not text:
        return ""
    
    # Characters to escape: # $ % & _ { } ~ ^ \
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

@app.route("/generate-pdf", methods=["POST"])
def generate_resume():
    try:
        # Get the data from the request
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # Extract the basic info
        name = escape_latex(data.get("name", "Your Name"))
        phone = escape_latex(data.get("phone", "123-456-7890"))
        email = escape_latex(data.get("email", "example@email.com"))
        linkedin = escape_latex(data.get("linkedin", ""))
        github = escape_latex(data.get("github", ""))
        
        # Process education
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
        
        # Process experience
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
            
            # Add bullet points
            for bullet in exp.get("bullets", []):
                bullet_text = escape_latex(bullet)
                experience_latex += f"""
        \\resumeItem{{{bullet_text}}}"""
            
            experience_latex += """
      \\resumeItemListEnd"""
        
        # Process projects
        projects_latex = ""
        for proj in data.get("projects", []):
            name = escape_latex(proj.get("name", ""))
            technologies = escape_latex(proj.get("technologies", ""))
            dates = escape_latex(proj.get("dates", ""))
            
            projects_latex += f"""
    \\resumeProjectHeading
      {{\\textbf{{{name}}} $|$ \\emph{{{technologies}}}}}{{{dates}}}
      \\resumeItemListStart"""
            
            # Add bullet points
            for bullet in proj.get("bullets", []):
                bullet_text = escape_latex(bullet)
                projects_latex += f"""
        \\resumeItem{{{bullet_text}}}"""
            
            projects_latex += """
      \\resumeItemListEnd"""
        
        # Process skills
        skills_latex = ""
        for category, items in data.get("skills", {}).items():
            category_text = escape_latex(category)
            skills_list = [escape_latex(skill) for skill in items]
            skills_text = ", ".join(skills_list)
            
            skills_latex += f"     \\textbf{{{category_text}}}: {skills_text} \\\\\n"
        
        # Create the full LaTeX document
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

% Custom commands
\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubSubheading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \textit{\small#1} & \textit{\small #2} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & #2 \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubItem}[1]{\resumeItem{#1}\vspace{-4pt}}

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
        
        # Generate the PDF
        pdf_path = generate_pdf(latex_content)
        
        if pdf_path and os.path.exists(pdf_path):
            return send_file(pdf_path, as_attachment=True, download_name="resume.pdf")
        else:
            return jsonify({"error": "Failed to generate PDF"}), 500
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)