import os
from langchain_openai import ChatOpenAI
import logging
from dotenv import load_dotenv

load_dotenv()

class LLMModel:
    """
    A class to encapsulate the ChatOpenAI model initialization and logging setup for Langsmith.
    """

    def __init__(self, model_name: str = "gpt-4o", temperature: float = 0):
        """
        Initializes the LangsmithChatModel with the specified OpenAI model and parameters.

        :param model_name: The name of the OpenAI model to use (default is 'gpt-4o').
        :param temperature: The temperature for the model's output (default is 0).
        """
        self.model_name = model_name
        self.temperature = temperature
        self.api_key = os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")

        self.model = ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature,
            openai_api_key=self.api_key
        )
        
        self.setup_logging()

    def setup_logging(self):
        """
        Configures the logging for Langsmith.
        """
        logging.basicConfig(level=logging.INFO)
        logging.info("Langsmith logging initialized: HOWUP")

    def get_model(self):
        """
        Returns the ChatOpenAI model instance.

        :return: ChatOpenAI object.
        """
        return self.model
