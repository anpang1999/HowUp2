from langchain_openai import ChatOpenAI
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import Tool, create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

import os
import requests
import xmltodict

load_dotenv()

def agent_response(user_input):
    # Initialize Chat Model
    model = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

    # Define RAG Chain function
    def initialize_rag_chain(query):
        # Load FAISS vectorstore
        vectorstore = FAISS.load_local(
            folder_path='db/faiss',
            index_name='index',
            embeddings=OpenAIEmbeddings(),
            allow_dangerous_deserialization=True
        )

        # Define retriever
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

        return str(retriever.invoke(query))

    def fetch_patent_info(keyword):
    
        # REST API call URL
        base_url = "http://plus.kipris.or.kr/openapi/rest/patUtiModInfoSearchSevice/freeSearchInfo"
        
        # Set API Key
        api_key = os.getenv("KIPRIS_REST_KEY").replace("\"", "")
        
        # Construct URL
        query_url = f"{base_url}?word={keyword}&docsStart=1&docsCount=5&lastvalue=R&accessKey={api_key}"
        
        try:
            # Make API call
            response = requests.get(query_url)
            response.raise_for_status()  # Handle HTTP errors
        except requests.exceptions.RequestException as e:
            print(f"Error occurred during API request: {e}")
            return []
        
        # Convert XML response to Dictionary
        content = response.content
        dict_type = xmltodict.parse(content)
        
        # Extract key data from the dictionary
        try:
            PatentInfo = dict_type['response']['body']['items']['PatentUtilityInfo']
        except KeyError:
            PatentInfo = ""
        
        # Define key mappings
        key_mapping = {
            'Applicant': '출원인',
            'ApplicationNumber': '출원번호',
            'InventionName': '특허명',
            'Abstract': '초록',
            'RegistrationStatus': '등록상태'
        }
        
        context = str([{new_key: item[old_key] for old_key, new_key in key_mapping.items() if old_key in item} for item in PatentInfo])
        return context

    # Define Tools
    rag_chain_tool = Tool(
        name="Retrieval Augmented Generator",
        func=initialize_rag_chain,
        description="useful for providing insights into business and industry trends.",
        verbose=False,
    )

    google_search = GoogleSerperAPIWrapper()

    google_search_tool = Tool(
        name="Intermediate Answer",
        func=google_search.run,
        description="useful for when you need to ask with search",
        verbose=False,
    )

    patent_search_tool = Tool(
        name="Search Patent Information",
        func=fetch_patent_info,
        description="useful for finding information about existing patents",
        verbose=False,
    )

    tools = [
        google_search_tool,
        rag_chain_tool,
        patent_search_tool
    ]

    # Create Prompt Template
    react_prompt_template = """Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question. Always respond in Korean.
    Begin!

    Question: {input}
    Thought:{agent_scratchpad}"""

    prompt = PromptTemplate.from_template(react_prompt_template)

    # Create Search Agent
    search_agent = create_react_agent(model, tools, prompt)
    agent_executor = AgentExecutor(
        agent=search_agent,
        tools=tools,
        verbose=True,
        return_intermediate_steps=True,
        handle_parsing_errors=True
    )

    # Execute agent with user input and return response
    response = agent_executor.invoke({"input": user_input})
    return response['output']