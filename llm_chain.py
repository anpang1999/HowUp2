from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# 환경변수 불러오기
load_dotenv()

# RAG 체인 함수 정의
def initialize_rag_chain():
    # Load FAISS vectorstore
    vectorstore = FAISS.load_local(
        folder_path='db/faiss',
        index_name='index',
        embeddings=OpenAIEmbeddings(),
        allow_dangerous_deserialization=True
    )

    # Retriever 정의
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # 프롬프트 템플릿 정의
    prompt = PromptTemplate.from_template(
        """
        당신은 질문에 따라 답변을 수행하는 친절한 AI 비서입니다. 당신은 주어진 context에서 주어진 question에 답하는 것을 수행합니다. 검색된 결과인 다음 context를 사용하여 질문인 question에 답하세요.
        context를 최대한 활용하여 답변해주세요.
        이름이나 기술적인 용어는 번역하지 않고 그대로 출력해주세요.

        # Question : {question}
        # Context : {context}
        # Answer : 
        """
    )

    # LLM 모델 초기화
    llm = ChatOpenAI(model='gpt-4o', temperature=0)

    # RAG Chain 반환
    return (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
