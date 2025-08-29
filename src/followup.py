from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_retrieval_chain, RetrievalQA
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain.chains import create_history_aware_retriever

def build_history_aware_chain(llm, retriever):
    system ="Formulate a standalone question given chat history and latest query."
    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])

    history_retriever = create_history_aware_retriever(llm=llm, retriever=retriever, prompt=prompt)

    # QA chain for retrieved docs
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant using context."),
        ("system", "Context: {context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])


    

    qa_chain = create_stuff_documents_chain(llm=llm, prompt=qa_prompt, document_variable_name="context")

    return create_retrieval_chain(history_retriever, qa_chain)
