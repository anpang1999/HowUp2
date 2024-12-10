# agent.py
from langchain_openai import ChatOpenAI
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import Tool, create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_teddynote import logging
import os
import requests
import xmltodict
import pickle # 객체 자체를 파일로 저장

from functools import lru_cache 
# 함수의 결과를 캐싱하여 반복 호출 시 성능을 향상시키는 데 사용하는 데코레이터를 제공하는 모듈
# LRU : Least Recently Used

load_dotenv()

CACHE_FILE_PATENT = "response_cache/response_cache_patent.pkl"
CACHE_FILE_SERP = "response_cache/response_cache_serp.pkl"

# 캐시 파일이 존재하면 읽어오고, 없으면 빈 딕셔너리로 초기화

if os.path.exists(CACHE_FILE_PATENT):
    with open(CACHE_FILE_PATENT, "rb") as f:
        response_cache_patent = pickle.load(f) 
else:
    response_cache_patent = {}  


if os.path.exists(CACHE_FILE_SERP):
    with open(CACHE_FILE_SERP, "rb") as f:
        response_cache_serp = pickle.load(f) 
else:
    response_cache_serp = {}

# 캐시 데이터를 파일에 저장하는 함수

def save_response_cache_patent():
    with open(CACHE_FILE_PATENT, "wb") as f:
        pickle.dump(response_cache_patent, f)
        # Python 객체 obj를 파일 객체 file에 저장

def save_response_cache_serp():
    with open(CACHE_FILE_SERP, "wb") as f:
        pickle.dump(response_cache_serp, f)


@lru_cache(maxsize=128)
# 데코레이터 실행함수, 함수 호출의 결과를 캐싱
def initialize_rag_chain(query):
    vectorstore = FAISS.load_local(
        folder_path='db/faiss',
        index_name='index',
        embeddings=OpenAIEmbeddings(),
        allow_dangerous_deserialization=True
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    return str(retriever.invoke(query))


def fetch_patent_info(keyword):
    # 키워드가 캐시에 있으면 해당 값을 반환
    if keyword in response_cache_patent:
        return response_cache_patent[keyword]

    base_url = "http://plus.kipris.or.kr/openapi/rest/patUtiModInfoSearchSevice/freeSearchInfo"
    api_key = os.getenv("KIPRIS_REST_KEY").replace("\"", "")
    query_url = f"{base_url}?word={keyword}&docsStart=1&docsCount=3&lastvalue=R&accessKey={api_key}"
    
    try:
        response = requests.get(query_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred during API request: {e}")
        return []

    content = response.content
    dict_type = xmltodict.parse(content)
    try:
        PatentInfo = dict_type['response']['body']['items']['PatentUtilityInfo']
    except KeyError:
        PatentInfo = ""
    
    key_mapping = {
        'Applicant': '출원인',
        'ApplicationNumber': '출원번호',
        'InventionName': '특허명',
        'Abstract': '초록',
        'RegistrationStatus': '등록상태'
    }
    context = str([{new_key: item[old_key] for old_key, new_key in key_mapping.items() if old_key in item} for item in PatentInfo])
    response_cache_patent[keyword] = context
    save_response_cache_patent()
    return context

def google_serper(query):
    if query in response_cache_serp:
        return response_cache_serp[query]
    
    response_cache_serp[query] = GoogleSerperAPIWrapper().run(query)

    save_response_cache_serp()
    return response_cache_serp[query]
    

def agent_response(user_input):
    
    model = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
    logging.langsmith("HOWUP")

    rag_chain_tool = Tool(
        name="Retrieval Augmented Generator",
        func=initialize_rag_chain,
        description="useful for providing insights into business and industry trends.",
        verbose=False,
    )

    google_search_tool = Tool(
        name="Google Search Tool",
        func=google_serper,
        description="useful for when you need to ask with search",
        verbose=False,
    )

    patent_search_tool = Tool(
        name="Search Patent Information",
        func=fetch_patent_info,
        description="useful for finding information about existing patents. The input must be written in Korean.",
        verbose=False,
    )

    tools = [
        google_search_tool,
        rag_chain_tool,
        patent_search_tool
    ]

     # Create Prompt Template
    react_prompt_template =  """ 
        You are an AI-Assistant with access to tools for answering questions effectively. Respond in Korean. Available tools: {tools}

        To use a tool, follow this format:

        '''
        Thought: Need a tool? Yes
        Action: [one of {tool_names}]
        Action Input: [input for the tool]
        Observation: [tool result]
        ... (repeat up to 3 times)
        '''

        If no tool is needed, respond as follows:

        '''
        Thought: Need a tool? No
        Final Answer: [response in Korean]
        '''

        Begin!

        Question: {input}
        Thought:{agent_scratchpad}
        """

    prompt = PromptTemplate.from_template(react_prompt_template)

    search_agent = create_react_agent(model, tools, prompt)
    
    agent_executor = AgentExecutor(
        agent=search_agent,
        tools=tools,
        verbose=True,
        return_intermediate_steps=True,
        handle_parsing_errors=True
    )

    response = agent_executor.invoke({"input": user_input})
    return response['output']