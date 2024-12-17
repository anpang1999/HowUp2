## faiss_storage/faiss_manager.py
from langchain_community.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

class FAISSManager:
    """Handles the storage and management of FAISS vector storage."""
    
    def __init__(self, db_path):
        self.db_path = db_path
    
    def store_documents(self, documents):
        """Store documents in FAISS index."""
        vectorstore = FAISS.from_documents(documents=documents, embedding=OpenAIEmbeddings())
        vectorstore.save_local(self.db_path)
        print("✅ FAISS database successfully saved.")