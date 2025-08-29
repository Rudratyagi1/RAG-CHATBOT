
import os
from langchain_community.document_loaders import PyPDFLoader

def load_documents(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    if not docs or not docs[0].page_content.strip():
        raise ValueError("No extractable text found.")
    return docs
