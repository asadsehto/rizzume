import os
import subprocess

def generate_pdf(latex_content):
    try:
        # Define the correct directory for PDF generation
        pdf_directory = "D:/Downloads/Projects/vs code/Rizzume"
        
        # Ensure the directory exists
        if not os.path.exists(pdf_directory):
            os.makedirs(pdf_directory)

        # Define the temporary file path for the LaTeX .tex file and the generated PDF
        tex_file_path = os.path.join(pdf_directory, "tmps2ovco65.tex")
        pdf_file_path = os.path.join(pdf_directory, "tmps2ovco65.pdf")

        # Write the LaTeX content to the .tex file
        with open(tex_file_path, 'w') as latex_file:
            latex_file.write(latex_content)

        # Run pdflatex to generate the PDF
        result = subprocess.run(['pdflatex', '-output-directory', pdf_directory, tex_file_path], capture_output=True, text=True)

        # Log output for debugging
        print(f"pdflatex output: {result.stdout}")
        print(f"pdflatex errors: {result.stderr}")

        # Check if PDF was generated
        if os.path.exists(pdf_file_path):
            print(f"PDF generated successfully. Size: {os.path.getsize(pdf_file_path)} bytes.")
            return pdf_file_path
        else:
            print("PDF generation failed.")
            return None

    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None
