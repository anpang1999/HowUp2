import sys
import html
import streamlit as st
sys.path.append('.')
from frontend.models.message import Message



class ChatUI:
    """
    A class to render the chat interface for user and system messages in a Streamlit app.
    """

    @staticmethod
    def render_custom_styles():
        """
        Applies custom CSS styles to the Streamlit app.

        This method defines and injects a style block for custom
        CSS to center images within the application.
        """
        st.markdown(
            """
            <style>
                .centered-image {
                    display: flex;
                    justify-content: center;
                    margin-top: 0;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def render_logo():
        """
        Renders the application logo at the top of the interface.

        The logo is displayed as a centered image with rounded corners.
        """
        st.markdown(
            """
            <div class="centered-image">
                <img src="https://i.ibb.co/Dw75bCW/how-up.png" alt="HowUp Logo" 
                style="max-width: 100%; height: auto; border-radius: 10px;">
            </div>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def render_message(message: Message):
        """
        Renders a chat message in the UI.

        Parameters:
            message (Message): A `Message` object containing the content and role.

        Behavior:
            - If the `role` is "user", the message appears on the right with a user icon.
            - If the `role` is anything else (e.g., "system"), the message appears on the left
              with a robot icon.

        The content of the message is sanitized to prevent injection of malicious HTML.

        Example:
            render_message(Message(role="user", content="Hello!"))
        """
        content = html.escape(message.content.strip())  # Escape HTML to prevent XSS attacks
        if message.role == "user":
            st.markdown(
                f"""
                <div style="display: flex; justify-content: flex-end; margin: 5px;">
                    <div style="background-color: #f1f1f1; color: black; padding: 10px; 
                    border-radius: 10px; max-width: 70%; text-align: left;">
                        {content}
                    </div>
                    <div style="margin-left: 10px; font-size: 20px;">👤</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style="display: flex; justify-content: flex-start; margin: 5px;">
                    <div style="margin-right: 10px; font-size: 20px;">🤖</div>
                    <div style="background-color: #e3e8ff; color: black; padding: 10px; 
                    border-radius: 10px; max-width: 70%; text-align: left;">
                        {content}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
