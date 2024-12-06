import streamlit as st
from llm_chain import initialize_rag_chain

# RAG 체인 초기화 - llm_chain 파일로부터 불러오기
rag_chain = initialize_rag_chain()

# Streamlit main함수 정의
def main():
    # 커스텀 헤더 스타일
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


    # chat_history 초기화
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # 사용자 질문 입력
    

    # 채팅 기록 화면 표시
    for message in st.session_state["chat_history"]:
        if message['role'] == "User" :
            with st.container():
            # 사용자 메시지를 오른쪽 정렬
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: flex-end; margin: 5px;">
                        <div style="background-color: #f1f1f1; color: black; padding: 10px; border-radius: 10px; max-width: 70%; text-align: left;">
                            {message['content']}
                    </div>
                    <div style="margin-left: 10px; font-size: 20px;">👤</div>
                </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            # 어시스턴트 메시지를 왼쪽 정렬
            st.markdown(
                f"""
                <div style="display: flex; justify-content: flex-start; margin: 5px;">
                    <div style="margin-right: 10px; font-size: 20px;">🤖</div>
                    <div style="background-color: #e3e8ff; color: black; padding: 10px; border-radius: 10px; max-width: 70%; text-align: left;">
                        {message['content']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if query := st.chat_input("채팅을 시작하세요!") :
        st.session_state["chat_history"].append({"role": "User", "content": query})
        
        with st.spinner("답변 생성 중..."):
            try:
                # 이전 대화 기록과 현재 질문을 함께 전달하여 LLM 모델 호출
                context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state["chat_history"]])
                answer = rag_chain.invoke(context)
                st.session_state["chat_history"].append({"role": "AI", "content": answer})
            except Exception as e:
                st.session_state["chat_history"].append({"role": "AI", "content": f"오류 발생: {e}"})
        st.rerun()
    else:
        st.warning("하고 싶은 질문이 있나요?")

# main 실행 함수
if __name__ == "__main__":
    main()
