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
