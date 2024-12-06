from langchain_openai import ChatOpenAI
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import Tool, create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

import os



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

    tools = [
        google_search_tool,
        rag_chain_tool
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