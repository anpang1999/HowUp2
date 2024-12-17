## embeddings/embedding_generator.py
import os
import re
import pdfplumber
from langchain.schema import Document

def get_filenames_in_folder(folder_path):
    """
    Get a list of all filenames in the specified folder.
    
    Args:
        folder_path (str): Path to the folder containing files.
    
    Returns:
        list: A list of filenames in the specified folder.
    """
    try:
        filenames = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
        return filenames
    except Exception as e:
        print(f"Error occurred: {e}")
        return []

def chunk_pdf_with_pdfplumber(file_path, start_page=1, end_page=-1):
    """
    Split a PDF into chunks of text from the specified page range.
    
    Args:
        file_path (str): Path to the PDF file.
        start_page (int): Starting page for extraction.
        end_page (int): Ending page for extraction.
    
    Returns:
        list: List of chunks extracted from the PDF.
    """
    chunks = []
    with pdfplumber.open(file_path) as pdf:
        total_pages = len(pdf.pages)
        if end_page < 0:
            end_page = total_pages + end_page + 1
        for page_num in range(start_page - 1, end_page):
            page = pdf.pages[page_num]
            text = page.extract_text()
            if text:
                cleaned_text = re.sub(r'\n|\r|\t', ' ', text)
                cleaned_text = re.sub(r'표<\d+-\d+>', '', cleaned_text)
                cleaned_text = re.sub(r'□| |○', '', cleaned_text)
                cleaned_text = re.sub(r'<(그림|표) \d+-\d+>', '', cleaned_text)
                chunks.append({
                    "page_content": cleaned_text.strip(),
                    "metadata": {
                        "source_type": "pdf",
                        "file_name": os.path.basename(file_path),
                        "page_number": page_num + 1,
                        "doc_id": f"{os.path.basename(file_path)}_page_{page_num + 1}"
                    }
                })
    return chunks

def add_pdf_to_documents(file_path, documents, start_page=1, end_page=-1):
    """
    Add chunks of a PDF to the documents list as Document objects.
    
    Args:
        file_path (str): Path to the PDF file.
        documents (list): List to append Document objects.
        start_page (int): Starting page for extraction.
        end_page (int): Ending page for extraction.
    """
    chunk_dicts = chunk_pdf_with_pdfplumber(file_path, start_page, end_page)
    new_documents = [
        Document(page_content=chunk["page_content"], metadata=chunk["metadata"])
        for chunk in chunk_dicts
    ]
    documents.extend(new_documents)