import os
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA , LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain_google_genai import GoogleGenerativeAI

def build_rag_chain(retriever):
    api_key = os.getenv("GOOGLE_API_KEY")
    llm = GoogleGenerativeAI(
        google_api_key=api_key,
        model="gemini-1.5-flash-latest",
        temperature=0.3
    )

    template = """
    You are an expert DevOps trainer. Answer the question based on the following context.

    If the context contains relevant information, use it to provide a comprehensive answer.
    If the context doesn't have the exact answer but has related information, use that to provide helpful guidance.
    

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    prompt = PromptTemplate(template=template, input_variables=["context", "Question"])

    llm_chain = LLMChain(llm=llm , prompt=prompt)


    doc_chain = StuffDocumentsChain(
        llm_chain=llm_chain,
        document_variable_name="context"
    )

    rag_chain = RetrievalQA(
        retriever=retriever,
        combine_documents_chain=doc_chain,
        return_source_documents=True
    )

    # Return both the retrieval chain and the raw LLM
    return rag_chain, llm
