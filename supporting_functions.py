##Import necessary library
from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import Chroma

from langchain_ollama import OllamaEmbeddings, OllamaLLM

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser

from langchain_core.runnables import RunnablePassthrough



EMBEDDING_MODEL = "nomic-embed-text"

LLM_MODEL = "llama3.2:1b"



def create_vector_store(file_path):

    loader = PyPDFLoader(file_path)

    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    splits = splitter.split_documents(docs)

    embedding = OllamaEmbeddings(
        model=EMBEDDING_MODEL
    )

    vector_store = Chroma.from_documents(
        splits,
        embedding,
        persist_directory="chroma_db"
    )

    return vector_store




def format_docs(docs):

    return "\n\n".join(doc.page_content for doc in docs)




def create_rag_chain(vector_store):

    llm = OllamaLLM(
        model=LLM_MODEL
    )

    retriever = vector_store.as_retriever()

    prompt = ChatPromptTemplate.from_template(
        """
Answer the question based only on the context below.

Context:
{context}

Question:
{question}
"""
    )

    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain