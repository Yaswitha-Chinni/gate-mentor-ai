from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_vector_store(embeddings, persist_directory="./chroma_db"):
    """
    Returns the Chroma vector store instance.
    """
    vector_store = Chroma(
        collection_name="study_buddy_collection",
        embedding_function=embeddings,
        persist_directory=persist_directory
    )
    return vector_store

def add_text_to_vector_store(text, vector_store):
    """
    Splits the text into chunks and adds them to the vector store.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    
    if chunks:
        vector_store.add_texts(texts=chunks)
        
def get_retriever(vector_store):
    """
    Returns a retriever for the vector store.
    """
    return vector_store.as_retriever(search_kwargs={"k": 3})
