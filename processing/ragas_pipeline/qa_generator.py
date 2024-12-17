## ragas_pipeline/qa_generator.py
from ragas.testset.generator import TestsetGenerator
from ragas.testset.evolutions import simple, reasoning, multi_context, conditional
from ragas.testset.extractor import KeyphraseExtractor
from ragas.testset.docstore import InMemoryDocumentStore
from langchain_openai import ChatOpenAI

class QAGenerator:
    """Handles the generation of Q&A pairs for the RAGAS pipeline."""
    
    def __init__(self, documents):
        self.documents = documents
        self.generator_llm = ChatOpenAI(model='gpt-4o')
        self.critic_llm = ChatOpenAI(model='gpt-4o')
    
    def generate_testset(self):
        """Generate the test set using RAGAS TestsetGenerator."""
        docstore = InMemoryDocumentStore()
        keyphrase_extractor = KeyphraseExtractor(llm=self.generator_llm)
        generator = TestsetGenerator.from_langchain(self.generator_llm, self.critic_llm, docstore=docstore)
        
        testset = generator.generate_with_langchain_docs(
            documents=self.documents, 
            test_size=5, 
            distributions={simple: 0.4, reasoning: 0.2, multi_context: 0.2, conditional: 0.2}, 
            with_debugging_logs=True
        )
        return testset.to_pandas()