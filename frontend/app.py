import streamlit as st
from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI
from ui.chat_ui import ChatUI
from models.chat_session import ChatSessionState
from models.message import Message
from backend.agent import AgentResponse
from pydantic import ValidationError


class ChatApp:
    """
    A Streamlit-based chat application that integrates an AI model with memory
    to maintain conversation history and provide intelligent responses.
    """

    def __init__(self):
        """
        Initializes the chat application, including session state and memory.

        If the session state is not already initialized, this method sets up:
        - A ConversationSummaryMemory to store and summarize chat history.
        - A ChatSessionState object to manage memory and displayed messages.

        Raises:
            ValidationError: If the session state initialization fails.
        """
        if "session_state" not in st.session_state:
            memory = ConversationSummaryMemory(
                llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0),
                return_messages=True,
            )
            st.session_state.session_state = ChatSessionState(
                memory=memory, messages_displayed=[]
            )
        try:
            self.session_state: ChatSessionState = st.session_state.session_state
        except ValidationError as e:
            st.error(f"Invalid session state: {e}")
            raise

    def handle_user_input(self, query: str):
        """
        Processes user input and generates an AI response.

        Args:
            query (str): The user's input message.

        Behavior:
            - Adds the user's message to the conversation memory.
            - Generates an AI response using the `agent_response` function.
            - Adds both the user's and the AI's messages to the displayed messages.

        Error Handling:
            - If an exception occurs during response generation, an error
              message is displayed to the user.
        """
        # Add the user's message to the session state and memory
        user_message = Message(role="user", content=query)
        self.session_state.memory.chat_memory.add_user_message(query)
        self.session_state.messages_displayed.append(user_message)

        # Generate AI response with a loading spinner
        with st.spinner("답변 생성 중..."):
            try:
                ai_response = AgentResponse.agent_response(str(self.session_state.memory.chat_memory))
                ai_response = ai_response.strip().replace("'''", "")  # Clean up response

                # Add AI response to the session state and memory
                assistant_message = Message(role="assistant", content=ai_response)
                self.session_state.memory.chat_memory.add_ai_message(ai_response)
                self.session_state.messages_displayed.append(assistant_message)
            except Exception as e:
                # Handle errors by displaying an error message
                error_message = Message(role="assistant", content=f"An error occurred: {e}")
                self.session_state.messages_displayed.append(error_message)

    def render_chat_history(self):
        """
        Renders the chat history, displaying all messages in the session state.
        """
        for message in self.session_state.messages_displayed:
            ChatUI.render_message(message)

    def run(self):
        """
        Runs the main chat application.

        The UI includes:
        - Custom styles and a logo at the top of the page.
        - A chat input box where users can enter messages.
        - A chat history display for user and AI messages.
        """
        # Render custom styles and the application logo
        ChatUI.render_custom_styles()
        ChatUI.render_logo()

        # Handle user input from the chat input box
        if query := st.chat_input("Start chatting!"):
            self.handle_user_input(query)
            st.rerun()  # Refresh the app to display the new message
        else:
            st.warning("💡당신의 아이디어는 무엇인가요?")

        # Display the chat history
        self.render_chat_history()


# Main entry point for the application
if __name__ == "__main__":
    app = ChatApp()

    try:
        app.run()
    except st.runtime.scriptrunner.StopException:
        # Gracefully handle Streamlit's StopException during reruns
        pass
