from functools import lru_cache
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

class RetrieverFAISS:
    def __init__(self, folder_path='db/faiss', index_name='index', cache_size=128):
        """
        RAG 체인 초기화를 위한 클래스입니다.
        :param folder_path: FAISS 데이터베이스 경로
        :param index_name: 인덱스 이름
        :param cache_size: 캐시 크기
        """
        self.folder_path = folder_path
        self.index_name = index_name
        self.cache = lru_cache(maxsize=cache_size)(self._initialize_retriever)

    def _initialize_retriever(self, query):
        """
        내부 메서드: FAISS 데이터를 로드하고 검색기를 생성합니다.
        :param query: 입력 쿼리
        :return: 검색 결과 문자열
        """
        vectorstore = FAISS.load_local(
            folder_path=self.folder_path,
            index_name=self.index_name,
            embeddings=OpenAIEmbeddings(),
            allow_dangerous_deserialization=True
        )
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        return str(retriever.invoke(query))

    def get_retrievar_result(self, query):
        """
        캐싱된 RAG 체인 검색 결과를 반환합니다.
        :param query: 입력 쿼리
        :return: 검색 결과 문자열
        """
        return self.cache(query)
