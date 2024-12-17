## run_all_RAG.py
import os
from dotenv import load_dotenv
from embeddings.embedding_generator import EmbeddingGenerator
from faiss_storage.faiss_manager import FAISSManager
from ragas_pipeline.ragas_pipeline import RAGASPipeline

# Load environment variables from .env file
load_dotenv()

def main():
    """Main entry point for running the entire RAG pipeline."""
    pdf_folder = './pdfs'
    db_path = './db/faiss'
    
    # 1. Generate embeddings for PDF files
    embedding_generator = EmbeddingGenerator(pdf_folder)
    documents = embedding_generator.generate_embeddings()
    
    # 2. Store the documents in FAISS index
    faiss_manager = FAISSManager(db_path)
    faiss_manager.store_documents(documents)
    
    # 3. Execute the RAGAS pipeline for evaluation
    ragas_pipeline = RAGASPipeline(documents)
    ragas_pipeline.execute_pipeline()

if __name__ == "__main__":
    main()