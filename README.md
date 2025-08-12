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

## Commands:

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

## 📝 Examples

### Extract text from a PDF:
```bash
python main.py extract document.pdf
```

### Extract text from specific pages:
```bash
python main.py extract document.pdf -s 5 -e 10
```

### Extract text and save to a specific file:
```bash
python main.py extract document.pdf -o extracted_text.txt
```

### Extract text from an encrypted PDF:
```bash
python main.py extract encrypted.pdf -p mypassword
```

### Extract text matching a pattern:
```bash
python main.py extract document.pdf -r "email: \S+@\S+\.\S+"
```

### Extract emails and save as JSON:
```bash
python main.py extract document.pdf -r "\S+@\S+\.\S+" -f json -o emails.json
```

### Extract document information:
```bash
python main.py info document.pdf
```

### Save document information to a file:
```bash
python main.py info document.pdf -o document_info.json
```

### Process all PDFs in a directory:
```bash
python main.py batch pdf_directory
```

### Process multiple specific PDF files:
```bash
python main.py batch "file1.pdf file2.pdf file3.pdf"
```

### Process PDFs recursively in all subdirectories:
```bash
python main.py batch pdf_directory -r
```

## 🧩 Advanced Usage

### Working with Regular Expressions

You can use regular expressions to extract specific patterns from PDFs:

- Extract all email addresses:
  ```bash
  python main.py extract document.pdf -r "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
  ```
  
- Extract phone numbers:
  ```bash
  python main.py extract document.pdf -r "\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
  ```

- Extract URLs:
  ```bash
  python main.py extract document.pdf -r "https?://[^\s]+"
  ```
  
### Processing Large Files

For very large PDF files, you may want to extract text page by page:
```bash
# Extract text from pages 1-10
python main.py extract large.pdf -o large_part1.txt -s 1 -e 10
```
```bash
# Extract text from pages 11-20
python main.py extract large.pdf -o large_part2.txt -s 11 -e 20
```

### Using with Other Tools

The extracted text can be piped to other command-line tools:

```bash
# Count words in a PDF
python main.py extract document.pdf -o - | wc -w
```
```bash
# Search for a keyword in a PDF
python main.py extract document.pdf -o - | grep "keyword"
```

## ⚠️ Limitations

- Some PDFs with complex layouts or scanned images may not extract perfectly
- PDFs with custom fonts or unusual encodings might have character conversion issues
- Very large PDFs may require significant memory resources
- Some heavily protected PDFs may not be accessible even with the correct password

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

Have fun!
