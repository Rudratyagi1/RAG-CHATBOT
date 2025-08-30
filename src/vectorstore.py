
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def build_vectorstore(chunks: list[Document], persist_dir: str="./chroma_db"):
    vect = Chroma.from_documents(
        documents=chunks,
        embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001"),
        persist_directory=persist_dir
    )
    vect.persist()
    return vect.as_retriever(search_type="similarity", search_kwargs={"k":5})
