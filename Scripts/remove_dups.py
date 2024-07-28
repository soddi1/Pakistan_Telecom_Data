import os
import hashlib
from PyPDF2 import PdfReader

def hash_pdf_content(file_path):
    """Generate a hash for the content of a PDF file."""
    try:
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            content = ""
            for page in reader.pages:
                content += page.extract_text() or ""
            return hashlib.md5(content.encode('utf-8')).hexdigest()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def remove_duplicate_pdfs(directory):
    """Remove PDFs with duplicate content in the given directory and its subdirectories."""
    pdf_hashes = {}
    files_to_remove = []

    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.pdf'):
                file_path = os.path.join(root, filename)
                file_hash = hash_pdf_content(file_path)

                if file_hash:
                    if file_hash in pdf_hashes:
                        files_to_remove.append(file_path)
                    else:
                        pdf_hashes[file_hash] = file_path

    for file_path in files_to_remove:
        print(f"Removing duplicate file: {file_path}")
        os.remove(file_path)

directory = r'C:\Users\Dell\Desktop\A_Project\Flooding\OpenCelliD data\Flooding\telecome_info\PTA-dataset\2024\output'
remove_duplicate_pdfs(directory)

