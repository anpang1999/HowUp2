from typing import List, Dict
from langchain.memory import ConversationSummaryMemory
from frontend.models.message import Message


class ChatSessionState:
    """
    Manages the state of a chat session, including conversation memory and 
    the list of messages displayed during the session.

    Attributes:
        memory (ConversationSummaryMemory): The object managing conversation summaries.
        messages_displayed (List[Message]): A list of Message objects currently displayed.
    """

    def __init__(self, memory: ConversationSummaryMemory, messages_displayed: List[Dict]) -> None:
        """
        Initializes the ChatSessionState with a memory object and a list of displayed messages.

        Args:
            memory (ConversationSummaryMemory): The conversation memory object.
            messages_displayed (List[Dict]): A list of dictionaries representing messages. 
                                             Each dictionary is converted to a Message object.
        """
        self.memory = memory
        self.messages_displayed = [Message(**msg) for msg in messages_displayed]
