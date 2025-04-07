from flask import Flask, request, send_file, jsonify
import os
import subprocess
import uuid
import tempfile
from flask_cors import CORS
from weasyprint import HTML

app = Flask(__name__)
CORS(app)  # Allow all domains

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


def generate_pdf_from_html(html_content):
    try:
        # Use Python's tempfile module to create temporary files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Generate unique filenames
            unique_id = str(uuid.uuid4())[:8]
            pdf_filename = f"resume_{unique_id}.pdf"
            
            pdf_file_path = os.path.join(temp_dir, pdf_filename)
            
            # Convert HTML to PDF using WeasyPrint
            HTML(string=html_content).write_pdf(pdf_file_path)
            
            # Check if PDF was created
            if os.path.exists(pdf_file_path):
                return pdf_file_path
            else:
                return None
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
    <div class="resume-section">
        <p><strong>{institution}</strong> - {degree} ({dates})</p>
        <p>{location}</p>
    </div>"""

        # Experience
        experience_latex = ""
        for exp in data.get("experience", []):
            position = escape_latex(exp.get("position", ""))
            dates = escape_latex(exp.get("dates", ""))
            company = escape_latex(exp.get("company", ""))
            location = escape_latex(exp.get("location", ""))

            experience_latex += f"""
    <div class="resume-section">
        <p><strong>{position}</strong> at {company} ({dates})</p>
        <p>{location}</p>
        <ul>"""

            for bullet in exp.get("bullets", []):
                bullet_text = escape_latex(bullet)
                experience_latex += f"""
            <li>{bullet_text}</li>"""

            experience_latex += "</ul></div>"

        # Projects
        projects_latex = ""
        for proj in data.get("projects", []):
            proj_name = escape_latex(proj.get("name", ""))
            technologies = escape_latex(proj.get("technologies", ""))
            dates = escape_latex(proj.get("dates", ""))

            projects_latex += f"""
    <div class="resume-section">
        <p><strong>{proj_name}</strong> - {technologies} ({dates})</p>
        <ul>"""

            for bullet in proj.get("bullets", []):
                bullet_text = escape_latex(bullet)
                projects_latex += f"""
            <li>{bullet_text}</li>"""

            projects_latex += "</ul></div>"

        # Skills
        skills_latex = ""
        for category, items in data.get("skills", {}).items():
            category_text = escape_latex(category)
            skills_list = [escape_latex(skill) for skill in items]
            skills_text = ", ".join(skills_list)
            skills_latex += f"<p><strong>{category_text}</strong>: {skills_text}</p>\n"

        # Final HTML content for the PDF
        html_content = f"""
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }}
        .resume-section {{
            margin-bottom: 20px;
        }}
        .resume-section p {{
            margin: 5px 0;
        }}
        .resume-section ul {{
            margin: 5px 0;
            padding-left: 20px;
        }}
    </style>
</head>
<body>
    <div class="resume-header">
        <h1>{name}</h1>
        <p>{phone} | <a href="mailto:{email}">{email}</a> | <a href="https://linkedin.com/in/{linkedin}">LinkedIn</a> | <a href="https://github.com/{github}">GitHub</a></p>
    </div>

    <h2>Education</h2>
    {education_latex}

    <h2>Experience</h2>
    {experience_latex}

    <h2>Projects</h2>
    {projects_latex}

    <h2>Skills</h2>
    {skills_latex}
</body>
</html>
"""

        pdf_path = generate_pdf_from_html(html_content)

        if pdf_path and os.path.exists(pdf_path):
            return send_file(pdf_path,
                             as_attachment=True,
                             download_name="resume.pdf",
                             mimetype="application/pdf")
        else:
            return jsonify({"error": "Failed to generate PDF"}), 500

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
