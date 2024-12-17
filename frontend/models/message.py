from pydantic import BaseModel


class Message(BaseModel):
    """
    Represents a message exchanged in a chat session.

    Attributes:
        role (str): The role of the message sender (e.g., "user", "assistant").
        content (str): The textual content of the message.
    """

    role: str
    content: str