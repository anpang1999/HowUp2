import streamlit as st
from agent import agent_response
from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI
import html


# Define the main function for the Streamlit app
def main():
    # Custom header styling
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

    st.markdown(
        """
        <div class="centered-image">
            <img src="https://i.ibb.co/Dw75bCW/how-up.png" alt="HowUp Logo" style="max-width: 100%; height: auto; border-radius: 10px;">
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Initialize chat history and session state
    if 'memory' not in st.session_state:
        st.session_state.memory = ConversationSummaryMemory(llm=ChatOpenAI(model='gpt-3.5-turbo',temperature=0), return_messages = True)

    if 'messages_displayed' not in st.session_state:
        st.session_state.messages_displayed = []

    # Handle user input
    if query := st.chat_input("채팅을 시작하세요!") :
        # Add the user's message to chat memory   
        st.session_state.memory.chat_memory.add_user_message(query)
        st.session_state.messages_displayed.append({'role' : 'user','content' : query})

        # Generate a response from the AI
        with st.spinner("답변 생성 중..."):
            try:
                # Pass chat history and user query to the LLM model
                answer = agent_response(str(st.session_state.memory.chat_memory))
                answer = answer.strip().replace("'''", "")
                st.session_state.memory.chat_memory.add_ai_message(answer)
                st.session_state.messages_displayed.append({'role' : 'assistant', 'content' : answer})
            except Exception as e:
                # Handle errors gracefully
                st.session_state.messages_displayed.append({"role": 'assistant', "content": f"오류 발생: {e}"})
        # Rerun the app to display updates
        st.rerun()
    else:
        # Prompt the user to enter a question
        st.warning("하고 싶은 질문이 있나요?")

    # Display chat history on the screen
    for message in st.session_state.messages_displayed:
        content = html.escape(message['content'].strip())
        if message['role'] == "user" :
            with st.container():
            # Render user messages aligned to the right
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: flex-end; margin: 5px;">
                        <div style="background-color: #f1f1f1; color: black; padding: 10px; border-radius: 10px; max-width: 70%; text-align: left;">
                            {content}
                    </div>
                    <div style="margin-left: 10px; font-size: 20px;">👤</div>
                </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            # Render assistant messages aligned to the left
            st.markdown(
                f"""
                <div style="display: flex; justify-content: flex-start; margin: 5px;">
                    <div style="margin-right: 10px; font-size: 20px;">🤖</div>
                    <div style="background-color: #e3e8ff; color: black; padding: 10px; border-radius: 10px; max-width: 70%; text-align: left;">
                        {content}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# Execute the main function
if __name__ == "__main__":
    main()