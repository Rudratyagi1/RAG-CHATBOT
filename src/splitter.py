
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

def split_documents(docs: list[Document], chunk_size=2000, chunk_overlap=400):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    return splitter.split_documents(docs)
