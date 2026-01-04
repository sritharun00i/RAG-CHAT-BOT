import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_core.runnables import Runnable

def build_chain(retriever) -> Runnable:
    """
    Build the RAG chain.
    """
    # Ensure OPENAI_API_KEY is present
    if not os.getenv("OPENAI_API_KEY"):
         print("Warning: OPENAI_API_KEY not found in environment variables.")

    # Initialize LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo")

    # Define prompt template
    prompt = ChatPromptTemplate.from_template("""
        Answer the following question based only on the provided context:

        <context>
        {context}
        </context>

        Question: {input}
    """)

    # Create the document chain (stuff documents into context)
    document_chain = create_stuff_documents_chain(llm, prompt)

    # Create the retrieval chain
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    return retrieval_chain
