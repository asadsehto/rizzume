import os
import subprocess
import uuid

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
        pdf_file_path = os.path.join(pdf_directory, f"{base_filename}.pdf")
        
        # Write the LaTeX content to the .tex file
        with open(tex_file_path, 'w', encoding='utf-8') as latex_file:
            latex_file.write(latex_content)
        
        # Change to the output directory before running pdflatex
        original_dir = os.getcwd()
        os.chdir(pdf_directory)
        
        try:
            # Run pdflatex to generate the PDF
            # -interaction=nonstopmode continues processing even if there are errors
            # We don't use -output-directory because we're already in the right directory
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', tex_file_path],
                capture_output=True, 
                text=True
            )
            
            # Log output for debugging
            print(f"pdflatex stdout: {result.stdout[:200]}...") # Print just the beginning to avoid cluttering logs
            print(f"pdflatex stderr: {result.stderr[:200]}...") # Print just the beginning to avoid cluttering logs
            
            # Check if pdflatex returned an error code
            if result.returncode != 0:
                print(f"pdflatex returned error code: {result.returncode}")
                
                # Look for the log file to provide more useful debugging info
                log_file_path = os.path.join(pdf_directory, f"{base_filename}.log")
                if os.path.exists(log_file_path):
                    with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as log_file:
                        log_content = log_file.read()
                        print(f"LaTeX log file excerpt: {log_content[-500:]}") # Print the end of the log
            
            # Check if PDF was generated
            pdf_file_path = os.path.join(pdf_directory, f"{base_filename}.pdf")
            if os.path.exists(pdf_file_path):
                print(f"PDF generated successfully. Path: {pdf_file_path}")
                print(f"PDF size: {os.path.getsize(pdf_file_path)} bytes.")
                return pdf_file_path
            else:
                print("PDF file not found after pdflatex execution.")
                return None
                
        finally:
            # Change back to the original directory
            os.chdir(original_dir)
            
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None