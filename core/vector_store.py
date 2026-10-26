import os
from langchain_chroma import Chroma
# Updated import to resolve the deprecation warning
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

CHROMA_DIR= "vector_db"
COLLECTION_NAME= "meeting_transcript"
# Updated model name to resolve the 401 Unauthorized error
EMBEDDING_MODEL= "sentence-transformers/all-MiniLM-L6-v2"


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"}
        )

def build_vector_store(transcripts: str) -> Chroma:
    print("Building vector store...")

    splitter= RecursiveCharacterTextSplitter(
        chunk_size= 500,
        chunk_overlap= 50
    )

    chunks= splitter.split_text(transcripts)

    # Renamed the iteration variable to 'c' to avoid shadowing the 'chunks' list
    docs= [Document(page_content= c, metadata={"chunk_index": i}) for i, c in enumerate(chunks)]

    embeddings= get_embeddings()
    vector_store= Chroma.from_documents(
        documents= docs,
        embedding= embeddings,
        collection_name= COLLECTION_NAME,
        persist_directory= CHROMA_DIR
    )

    return vector_store


def load_vector_store() -> Chroma:
    embeddings = get_embeddings()
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )
    return vector_store

def get_retriever(vector_store: Chroma, k: int = 3):
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )
    return retriever