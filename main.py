import streamlit as st
import os
from supporting_functions import create_vector_store, create_rag_chain

st.set_page_config(page_title="RAG with Ollama & ChromaDB", layout="wide")
st.title("📄 RAG Project with Ollama & ChromaDB")
st.write("""
Upload a PDF and ask questions about its content.
The system uses a local Ollama model (LLaMA3.2) and ChromaDB.
""")

# Sidebar for uploading PDF
with st.sidebar:
    st.header("Upload Your Document")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    process_button = st.button("Process")

# Initialize session state
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None

# Process uploaded PDF
if process_button and uploaded_file:
    with st.spinner("Processing document..."):
        temp_dir = "temp_docs"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Create vector store & RAG chain
        st.session_state.vector_store = create_vector_store(file_path)
        st.session_state.rag_chain = create_rag_chain(st.session_state.vector_store)
        st.success("Document processed successfully!")
if st.session_state.rag_chain:
    question = st.text_input("Ask your question")

    if st.button("Get Answer") and question:
        with st.spinner("Thinking..."):
            # Invoke RAG chain
            response = st.session_state.rag_chain.invoke(question)
            st.subheader("Answer")
            st.write(response)

            # Show context used
            docs = st.session_state.vector_store.similarity_search(question, k=5)
            with st.expander("Context"):
                for doc in docs:
                    st.info(doc.page_content)
# Question input and answer
# if st.session_state.rag_chain:
#     question = st.text_input("Ask your question")

#     if st.button("Get Answer") and question:
#         with st.spinner("Thinking..."):
#             # Invoke RAG chain
#             response = st.session_state.rag_chain.invoke(question)
#             st.subheader("Answer")
#             st.write(response)

#             # Show context used
#             with st.expander("Context"):
#                 retriever = st.session_state.vector_store.as_retriever()
#                 docs = retriever.retrieve(question)  # <-- fixed line
#                 for doc in docs:
#                     st.info(doc.page_content)
# if st.session_state.rag_chain:
#     question = st.text_input("Ask your question")

#     if st.button("Get Answer") and question:
#         with st.spinner("Thinking..."):
#             # Invoke chain
#             response = st.session_state.rag_chain.invoke(question)
#             st.subheader("Answer")
#             st.write(response)

#             # Show context used
#             with st.expander("Context"):
#                 docs = st.session_state.vector_store.as_retriever().get_relevant_documents(question)
#                 for doc in docs:
#                     st.info(doc.page_content)