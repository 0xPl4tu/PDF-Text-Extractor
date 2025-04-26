# 📄 PDF Text Extractor

A versatile command-line tool for extracting text and metadata from PDF files with support for pattern matching and batch processing.

## ✨ Features

- 📃 Extract text from PDF files with page range selection
- 🔍 Extract specific content using regular expressions
- 🔐 Support for encrypted PDF files with password protection
- ℹ️ Extract metadata and document information
- 📊 Output results in various formats (text, JSON, CSV)
- 🔄 Process multiple PDF files in batch mode
- 📁 Recursive directory search for batch processing

## 📋 Requirements

- Python 3.6 or higher
- PyPDF2 library

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/0xPl4tu/pdf-text-extractor.git
cd pdf-text-extractor
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Make the script executable (Unix/Linux/macOS):
```bash
chmod +x main.py
```

## 🔍 Usage

```bash
python main.py <command> [options]
```

### Commands:

- `extract`: Extract text from a PDF file
- `info`: Extract metadata from a PDF file
- `batch`: Extract text from multiple PDF files

## ⚙️ Options

### Extract Command Options:
- `pdf`: PDF file path (required)
- `-o, --output`: Output file path (default: extracted_pdf.txt)
- `-s, --start-page`: Start page number (default: 1)
- `-e, --end-page`: End page number (default: last page)
- `-p, --password`: Password for encrypted PDF
- `-r, --regex`: Regular expression pattern to extract specific text
- `-f, --format`: Output format for regex matches (text, json, csv)

### Info Command Options:
- `pdf`: PDF file path (required)
- `-o, --output`: Output file path (default: print to console)
- `-p, --password`: Password for encrypted PDF

### Batch Command Options:
- `pdf_dir`: Directory containing PDF files or space-separated list of PDF files
- `-o, --output-dir`: Output directory (default: extracted_pdfs)
- `-p, --password`: Password for encrypted PDFs
- `-r, --recursive`: Recursively search for PDF files in subdirectories