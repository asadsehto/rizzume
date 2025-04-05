from flask import Flask, request, send_file
import os
from latex_utils import generate_pdf  # Assuming this is your PDF generation function

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to Rizzume - Resume Generator API!"

@app.route("/generate-pdf", methods=["POST"])
def generate_resume():
    # Get the form data from the POST request
    data = request.get_json()
    name = data.get("name")
    phone = data.get("phone")
    email = data.get("email")
    linkedin = data.get("linkedin")
    github = data.get("github")
    education = data.get("education")
    experience = data.get("experience")
    skills = data.get("skills")
    projects = data.get("projects")

    # Generate LaTeX content using the provided data
    latex_content = f"""
    \\documentclass[letterpaper,11pt]{{article}}

    \\usepackage{{latexsym}}
    \\usepackage[empty]{{fullpage}}
    \\usepackage{{titlesec}}
    \\usepackage{{marvosym}}
    \\usepackage[usenames,dvipsnames]{{color}}  
    \\usepackage{{verbatim}}
    \\usepackage{{enumitem}}
    \\usepackage[hidelinks]{{hyperref}}
    \\usepackage{{fancyhdr}}
    \\usepackage[english]{{babel}}
    \\usepackage{{tabularx}}
    \\input{{glyphtounicode}}

    \\pagestyle{{fancy}}
    \\fancyhf{{}} 
    \\fancyfoot{{}}
    \\renewcommand{{\\headrulewidth}}{{0pt}}
    \\renewcommand{{\\footrulewidth}}{{0pt}}

    \\addtolength{{\\oddsidemargin}}{{-0.5in}}
    \\addtolength{{\\evensidemargin}}{{-0.5in}}
    \\addtolength{{\\textwidth}}{{1in}}
    \\addtolength{{\\topmargin}}{{-.5in}}
    \\addtolength{{\\textheight}}{{1.0in}}

    \\urlstyle{{same}}

    \\raggedbottom
    \\raggedright
    \\setlength{{\\tabcolsep}}{{0in}}

    \\titleformat{{\\section}}{{\\vspace{{-4pt}}\\scshape\\raggedright\\large}}{{}}{{0em}}{{}}[\\color{{black}}\\titlerule \\vspace{{-5pt}}]

    \\pdfgentounicode=1

    \\newcommand{{\\resumeItem}}[1]{{\\item\\small{{#1 \\vspace{{-2pt}}}}}}

    \\newcommand{{\\resumeSubheading}}[4]{{\\vspace{{-2pt}}\\item
        \\begin{{tabular*}}{{0.97\\textwidth}}[t]{{l@{{\\extracolsep{{\\fill}}}}r}}
        \\textbf{{#1}} & #2 \\\\
        \\textit{{\\small#3}} & \\textit{{\\small #4}} \\\\
        \\end{{tabular*}}\\vspace{{-7pt}}}}

    \\newcommand{{\\resumeSubSubheading}}[2]{{\\item
        \\begin{{tabular*}}{{0.97\\textwidth}}{{l@{{\\extracolsep{{\\fill}}}}r}}
        \\textit{{\\small#1}} & \\textit{{\\small #2}} \\\\
        \\end{{tabular*}}\\vspace{{-7pt}}}}

    \\newcommand{{\\resumeProjectHeading}}[2]{{\\item
        \\begin{{tabular*}}{{0.97\\textwidth}}{{l@{{\\extracolsep{{\\fill}}}}r}}
        \\small#1 & #2 \\\\
        \\end{{tabular*}}\\vspace{{-7pt}}}}

    \\newcommand{{\\resumeSubItem}}[1]{{\\resumeItem{{#1}}\\vspace{{-4pt}}}}

    \\renewcommand\\labelitemii{{\\vcenter{{\\hbox{{\\tiny$\\bullet$}}}}}}

    \\newcommand{{\\resumeSubHeadingListStart}}{{\\begin{{itemize}}[leftmargin=0.15in, label={{}}]}}
    \\newcommand{{\\resumeSubHeadingListEnd}}{{\\end{{itemize}}}}
    \\newcommand{{\\resumeItemListStart}}{{\\begin{{itemize}}}}
    \\newcommand{{\\resumeItemListEnd}}{{\\end{{itemize}}}}\\vspace{{-5pt}}}}

    \\begin{{document}}

    \\begin{{center}}
        \\textbf{{\\Huge \\scshape {name}}} \\\\ \\vspace{{1pt}}
        \\small {phone} $|$ \\href{{mailto:{email}}}{{\\underline{{{email}}}}} $|$ 
        \\href{{https://linkedin.com/in/{linkedin}}}{{\\underline{{linkedin.com/in/{linkedin}}}}} $|$
        \\href{{https://github.com/{github}}}{{\\underline{{github.com/{github}}}}}
    \\end{{center}}

    \\section{{Education}}
    \\resumeSubHeadingListStart
        {education}
    \\resumeSubHeadingListEnd

    \\section{{Experience}}
    \\resumeSubHeadingListStart
        {experience}
    \\resumeSubHeadingListEnd

    \\section{{Projects}}
    \\resumeSubHeadingListStart
        {projects}
    \\resumeSubHeadingListEnd

    \\section{{Technical Skills}}
    \\begin{{itemize}}[leftmargin=0.15in, label={{}}]
        \\small{{\\item{{\\textbf{{Languages}}{{: Java, Python, C/C++, SQL (Postgres), JavaScript, HTML/CSS, R}}}}}} \\\\
        \\textbf{{Frameworks}}{{: React, Node.js, Flask, JUnit, WordPress, Material-UI, FastAPI}} \\\\
        \\textbf{{Developer Tools}}{{: Git, Docker, TravisCI, Google Cloud Platform, VS Code, Visual Studio, PyCharm, IntelliJ, Eclipse}} \\\\
        \\textbf{{Libraries}}{{: pandas, NumPy, Matplotlib}}
    \\end{{itemize}}

    \\end{{document}}
    """

    # Generate the PDF
    pdf_path = generate_pdf(latex_content)

    # Send the generated PDF file back to the user
    return send_file(pdf_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
