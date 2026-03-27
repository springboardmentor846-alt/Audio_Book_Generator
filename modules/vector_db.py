import chromadb
from sentence_transformers import SentenceTransformer
import streamlit as st


# ---------- LOAD EMBEDDING MODEL ONLY WHEN NEEDED ----------
@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


# ---------- LOAD CHROMA COLLECTION ----------
@st.cache_resource
def get_collection():
    client = chromadb.Client()
    return client.get_or_create_collection(name="documents")


# ---------- CHUNK TEXT ----------
def chunk_text(text, chunk_size=800):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    return chunks


# ---------- STORE DOCUMENT ----------
def store_document(text):

    embedding_model = load_embedding_model()
    collection = get_collection()

    chunks = chunk_text(text)

    embeddings = embedding_model.encode(chunks).tolist()

    ids = [f"id_{i}" for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )


# ---------- RETRIEVE RELEVANT CHUNKS ----------
def retrieve_chunks(question, k=3):

    embedding_model = load_embedding_model()
    collection = get_collection()

    query_embedding = embedding_model.encode([question]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k
    )

    return results["documents"][0]