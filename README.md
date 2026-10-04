# Rizzume

**A full-stack resume builder with React, Flask, and LaTeX PDF export.**

Enter education, experience, projects, and skills through a form-based interface, preview your resume, and download a formatted PDF.

## Features

- Resume sections for education, experience, projects, and skills.
- Add and remove entries as your resume changes.
- Real-time preview and PDF generation.
- Responsive React interface.

## Architecture

```text
React form → Flask API → LaTeX document → PDF download
```

| Layer | Technology |
| --- | --- |
| Interface | React, HTML, CSS |
| API | Python, Flask |
| PDF generation | LaTeX / pdflatex |
| Packaging | Dockerfile and deployment configuration |

## Development

```bash
git clone https://github.com/asadsehto/rizzume.git
cd rizzume
python -m venv .venv
```

Activate the environment, then start the root Python API:

```bash
python -m pip install -r requirements.txt
python main.py
```

The API defaults to port **8080**, configurable through `PORT`. PDF generation requires `pdflatex` and the LaTeX packages used by the resume template.

In a second terminal:

```bash
cd rizzume/frontend
npm install
npm start
```

Configure the frontend API base URL to match your backend.

## Repository map

- `frontend/` — React interface.
- `main.py` — root Flask API and PDF-generation entry point.
- `latex_utils.py` — LaTeX-related utilities.
- `Dockerfile`, `netlify.toml`, and Railway configuration — packaging and deployment setup.

## Usage

1. Enter your contact details.
2. Add education, experience, projects, and skills.
3. Review the preview.
4. Generate and download your PDF.

The project aims to produce readable resumes; compatibility with every applicant-tracking system is not guaranteed.

## Contributing

Issues and pull requests are welcome. Include reproduction steps for bugs and sample input with personal information removed.

## Contact

[Asad Saleem](https://github.com/asadsehto) · [Email](mailto:asadsaleemsahto@gmail.com)
