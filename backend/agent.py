from langchain.agents import create_react_agent, AgentExecutor

from backend.tools import retriever_faiss_tool,google_search_tool,patent_search_tool

from backend.llm_model import LLMModel
from backend.react_prompt import ReactPrompt
from dotenv import load_dotenv

load_dotenv()

class AgentResponse:

    
    
    def agent_response(user_input):
        
        tools = [retriever_faiss_tool, 
                 google_search_tool, 
                 patent_search_tool]
        
        llm_model_instance = LLMModel(model_name="gpt-4o", temperature=0)
    
        model = llm_model_instance.get_model()

        prompt_instance = ReactPrompt()

        prompt = prompt_instance.get_prompt()

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