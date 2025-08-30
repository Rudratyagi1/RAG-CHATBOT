
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def build_vectorstore(chunks: list[Document]):
    vect = Chroma.from_documents(
        documents=chunks,
        embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    )

    return vect.as_retriever(search_type="similarity", search_kwargs={"k":5})
