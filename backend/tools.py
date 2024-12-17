from langchain.agents import Tool
from utils.google_serper import GoogleSerper
from utils.fetch_patent_info import FetchPatentInfo
from utils.retriever_faiss import RetrieverFAISS

      

# 각 도구 인스턴스를 생성
retriever_faiss_instance = RetrieverFAISS()
retriever_faiss_tool = Tool(
    name="Retriever Augmented Generator",
    func=retriever_faiss_instance.get_retrievar_result,
    description="useful for providing insights into business and industry trends.",
    verbose=False,
)
google_serper_instance = GoogleSerper()
google_search_tool = Tool(
    name="Google Search Tool",
    func=google_serper_instance.google_serper,
    description="useful for when you need to ask with search",
    verbose=False,
)
fetch_patent_info_instance = FetchPatentInfo()
patent_search_tool = Tool(
    name="Search Patent Information",
    func=fetch_patent_info_instance.fetch_patent_info,
    description="useful for finding information about existing patents. The input must be written in Korean.",
    verbose=False,
)