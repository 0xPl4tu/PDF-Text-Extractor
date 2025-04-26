#!/usr/bin/env python3

import argparse
import os
import sys
import json
from datetime import datetime
import PyPDF2
import re
import csv

def extract_text_from_pdf(pdf_path, start_page=None, end_page=None, password=None):
    """Extract text from a PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            # Check if the PDF is encrypted
            if reader.is_encrypted:
                if password:
                    try:
                        reader.decrypt(password)
                    except:
                        print(f"Error: Incorrect password for {pdf_path}")
                        return None
                else:
                    print(f"Error: PDF {pdf_path} is encrypted and no password was provided")
                    return None
            
            # Get page range
            total_pages = len(reader.pages)
            start = start_page if start_page is not None else 1
            end = end_page if end_page is not None else total_pages
            
            # Validate page range
            if start < 1:
                start = 1
            if end > total_pages:
                end = total_pages
            if start > end:
                print(f"Error: Start page ({start}) is greater than end page ({end})")
                return None
            
            # Extract text from pages
            text = ""
            for page_num in range(start-1, end):
                try:
                    page = reader.pages[page_num]
                    text += page.extract_text() + "\n\n"
                except Exception as e:
                    print(f"Error extracting text from page {page_num+1}: {e}")
            
            return text
    except FileNotFoundError:
        print(f"Error: File {pdf_path} not found")
        return None
    except Exception as e:
        print(f"Error opening {pdf_path}: {e}")
        return None

def save_text(text, output_file):
    """Save extracted text to a file"""
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Text successfully saved to {output_file}")
    except Exception as e:
        print(f"Error saving text to {output_file}: {e}")

def extract_info(pdf_path, password=None):
    """Extract metadata from a PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            # Check if the PDF is encrypted
            if reader.is_encrypted:
                if password:
                    try:
                        reader.decrypt(password)
                    except:
                        print(f"Error: Incorrect password for {pdf_path}")
                        return None
                else:
                    print(f"Error: PDF {pdf_path} is encrypted and no password was provided")
                    return None
            
            # Get document info
            info = reader.metadata
            if info:
                info_dict = {
                    "Title": info.title if hasattr(info, 'title') else None,
                    "Author": info.author if hasattr(info, 'author') else None,
                    "Subject": info.subject if hasattr(info, 'subject') else None,
                    "Creator": info.creator if hasattr(info, 'creator') else None,
                    "Producer": info.producer if hasattr(info, 'producer') else None,
                    "Creation Date": info.creation_date.strftime("%Y-%m-%d %H:%M:%S") if hasattr(info, 'creation_date') and info.creation_date else None,
                    "Modification Date": info.modification_date.strftime("%Y-%m-%d %H:%M:%S") if hasattr(info, 'modification_date') and info.modification_date else None,
                    "Pages": len(reader.pages)
                }
                return info_dict
            else:
                return {"Pages": len(reader.pages)}
    except FileNotFoundError:
        print(f"Error: File {pdf_path} not found")
        return None
    except Exception as e:
        print(f"Error extracting info from {pdf_path}: {e}")
        return None

def extract_with_pattern(text, pattern, output_format=None, output_file=None):
    """Extract text matching a regex pattern"""
    if not text:
        return
    
    matches = re.findall(pattern, text)
    
    if not matches:
        print("No matches found for the given pattern")
        return
    
    if output_format == "json" and output_file:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump({"matches": matches}, file, indent=4)
        print(f"Matches saved to {output_file} in JSON format")
    elif output_format == "csv" and output_file:
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Match"])
            for match in matches:
                writer.writerow([match])
        print(f"Matches saved to {output_file} in CSV format")
    else:
        print("\nMatches found:")
        for i, match in enumerate(matches, 1):
            print(f"{i}. {match}")

def extract_multiple_pdfs(pdf_files, output_dir, password=None):
    """Extract text from multiple PDF files"""
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except Exception as e:
            print(f"Error creating output directory {output_dir}: {e}")
            return
    
    for pdf_path in pdf_files:
        try:
            if not os.path.exists(pdf_path):
                print(f"Warning: File {pdf_path} not found, skipping...")
                continue
            
            # Get base filename without extension
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            output_file = os.path.join(output_dir, f"{base_name}.txt")
            
            # Extract text
            text = extract_text_from_pdf(pdf_path, password=password)
            if text:
                save_text(text, output_file)
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Extract text from PDF files")
    
    # Main operation commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract text from a PDF file")
    extract_parser.add_argument("pdf", help="PDF file path")
    extract_parser.add_argument("-o", "--output", help="Output file path (default: extracted_pdf.txt)")
    extract_parser.add_argument("-s", "--start-page", type=int, help="Start page number (default: 1)")
    extract_parser.add_argument("-e", "--end-page", type=int, help="End page number (default: last page)")
    extract_parser.add_argument("-p", "--password", help="Password for encrypted PDF")
    extract_parser.add_argument("-r", "--regex", help="Regular expression pattern to extract specific text")
    extract_parser.add_argument("-f", "--format", choices=["text", "json", "csv"], default="text", 
                               help="Output format for regex matches (default: text)")
    
    # Info command
    info_parser = subparsers.add_parser("info", help="Extract metadata from a PDF file")
    info_parser.add_argument("pdf", help="PDF file path")
    info_parser.add_argument("-o", "--output", help="Output file path (default: print to console)")
    info_parser.add_argument("-p", "--password", help="Password for encrypted PDF")
    
    # Batch command
    batch_parser = subparsers.add_parser("batch", help="Extract text from multiple PDF files")
    batch_parser.add_argument("pdf_dir", help="Directory containing PDF files or space-separated list of PDF files")
    batch_parser.add_argument("-o", "--output-dir", default="extracted_pdfs", help="Output directory (default: extracted_pdfs)")
    batch_parser.add_argument("-p", "--password", help="Password for encrypted PDFs")
    batch_parser.add_argument("-r", "--recursive", action="store_true", help="Recursively search for PDF files in subdirectories")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "extract":
        # Set default output file if not specified
        output_file = args.output if args.output else "extracted_pdf.txt"
        
        # Extract text from PDF
        text = extract_text_from_pdf(args.pdf, args.start_page, args.end_page, args.password)
        
        if text:
            if args.regex:
                # Extract text matching regex pattern
                extract_with_pattern(text, args.regex, args.format, output_file)
            else:
                # Save full text
                save_text(text, output_file)
    
    elif args.command == "info":
        # Extract PDF metadata
        info = extract_info(args.pdf, args.password)
        
        if info:
            if args.output:
                # Save info to file
                try:
                    with open(args.output, 'w', encoding='utf-8') as file:
                        json.dump(info, file, indent=4)
                    print(f"PDF information saved to {args.output}")
                except Exception as e:
                    print(f"Error saving info to {args.output}: {e}")
            else:
                # Print info to console
                print("\nPDF Information:")
                max_key_length = max(len(key) for key in info.keys())
                for key, value in info.items():
                    print(f"{key:<{max_key_length + 2}}: {value}")
    
    elif args.command == "batch":
        # Check if input is a directory or list of files
        if os.path.isdir(args.pdf_dir):
            # Get all PDF files in directory
            pdf_files = []
            if args.recursive:
                for root, _, files in os.walk(args.pdf_dir):
                    for file in files:
                        if file.lower().endswith('.pdf'):
                            pdf_files.append(os.path.join(root, file))
            else:
                pdf_files = [os.path.join(args.pdf_dir, file) for file in os.listdir(args.pdf_dir) 
                           if file.lower().endswith('.pdf') and os.path.isfile(os.path.join(args.pdf_dir, file))]
            
            if not pdf_files:
                print(f"No PDF files found in {args.pdf_dir}")
                return
        else:
            # Assume it's a space-separated list of PDF files
            pdf_files = args.pdf_dir.split()
        
        # Extract text from multiple PDFs
        extract_multiple_pdfs(pdf_files, args.output_dir, args.password)

if __name__ == "__main__":
    main()
