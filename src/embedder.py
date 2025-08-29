'''import os
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings

def create_embeddings(chunks: list[str], model: str = "models/embedding-001"):
    # Load your Google API key from environment
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Environment variable GOOGLE_API_KEY is not set")

    # Instantiate embeddings with the correct parameter name
    embedding_client = GoogleGenerativeAIEmbeddings(model=model)

    # Embed documents
    return embedding_client.embed_documents(chunks)'''
