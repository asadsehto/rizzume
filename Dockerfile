FROM python:3.12.3-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-latex-extra \
    texlive-xetex \
    ghostscript \
    poppler-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install pdftoppm for debugging if needed
RUN apt-get update && apt-get install -y poppler-utils && apt-get clean

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create directory for temporary PDF files
RUN mkdir -p /tmp/pdfs && chmod 777 /tmp/pdfs

# Environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV TEMP_PDF_DIR=/tmp/pdfs

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Command to run the application
CMD ["python", "main.py"]
