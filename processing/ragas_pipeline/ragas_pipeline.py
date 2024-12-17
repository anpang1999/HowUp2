## ragas_pipeline/ragas_pipeline.py
from ragas_pipeline.qa_generator import QAGenerator
from ragas_pipeline.evaluator import Evaluator

class RAGASPipeline:
    """Handles the RAGAS-based Q&A generation and evaluation pipeline."""
    
    def __init__(self, documents):
        self.documents = documents
    
    def execute_pipeline(self):
        """Execute Q&A generation and evaluation pipeline."""
        # Step 1: Generate Q&A pairs
        qa_generator = QAGenerator(self.documents)
        test_df = qa_generator.generate_testset()
        
        # Step 2: Evaluate the performance of the Q&A pairs
        evaluator = Evaluator(test_df)
        results = evaluator.evaluate_performance()
        print("📘 Evaluation results: ", results.to_pandas())