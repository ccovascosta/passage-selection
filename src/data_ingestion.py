import os
from PyPDF2 import PdfFileReader
from docx import Document
from pptx import Presentation

def extract_metadata(file_path):
    metadata = {
        'filename': os.path.basename(file_path),
        'type': os.path.splitext(file_path)[1][1:],  # Get the file extension without the dot
        'title': None,
        'authors': None,
        'lastmodifiedtime': None
    }
    
    try:
        if file_path.endswith('.pdf'):
            with open(file_path, 'rb') as f:
                pdf = PdfFileReader(f)
                info = pdf.getDocumentInfo()
                metadata['title'] = info.title
                metadata['authors'] = info.author
                metadata['lastmodifiedtime'] = info.modDate
        elif file_path.endswith('.docx'):
            doc = Document(file_path)
            core_properties = doc.core_properties
            metadata['title'] = core_properties.title
            metadata['authors'] = core_properties.author
            metadata['lastmodifiedtime'] = core_properties.modified
        elif file_path.endswith('.pptx'):
            prs = Presentation(file_path)
            core_properties = prs.core_properties
            metadata['title'] = core_properties.title
            metadata['authors'] = core_properties.author
            metadata['lastmodifiedtime'] = core_properties.modified
    except Exception as e:
        print(f"Error extracting metadata from {file_path}: {e}")
    
    return metadata

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with open(file_path, "rb") as file:
            reader = PdfFileReader(file)
            for page_num in range(reader.numPages):
                text += reader.getPage(page_num).extractText()
    except Exception as e:
        print(f"Error extracting text from PDF {file_path}: {e}")
    return text

def extract_text_from_docx(file_path):
    text = ""
    try:
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error extracting text from DOCX {file_path}: {e}")
    return text

def extract_text_from_pptx(file_path):
    text = ""
    try:
        prs = Presentation(file_path)
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text += shape.text + "\n"
    except Exception as e:
        print(f"Error extracting text from PPTX {file_path}: {e}")
    return text

def load_documents(folder_path):
    documents = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_name.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif file_name.endswith('.docx'):
            text = extract_text_from_docx(file_path)
        elif file_name.endswith('.pptx'):
            text = extract_text_from_pptx(file_path)
        else:
            continue
        metadata = extract_metadata(file_path)
        documents.append((file_name, text, metadata))
    return documents
