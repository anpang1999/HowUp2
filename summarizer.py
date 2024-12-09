from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os


def hist_summarizer(chat_history):
    """
    Summarize the given chat history using the ChatOpenAI model.

    Parameters:
        chat_history (str): The chat history in the format "role: content\n".
        
    Returns:
        str: A summary of the chat history.
    """
    # 토큰 절약을 위한 gpt-3.5-turbo 모델 활용
    chat_model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
    
    # 대화 요약 요청 메시지
    system_message = SystemMessage(content="You are an assistant that summarizes chat history.")
    user_message = HumanMessage(content=f"Please summarize the following chat history:\n{chat_history}")

    # 모델에 메시지 전달 및 요약 생성
    response = chat_model([system_message, user_message])
    
    return response.content
