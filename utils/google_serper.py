# File: google_serper_manager.py

from utils.cache_manager import CacheManager
from langchain_community.utilities import GoogleSerperAPIWrapper

from dotenv import load_dotenv

load_dotenv()

class GoogleSerper:
    def __init__(self, cache_file="response_cache/response_cache_serp.pkl"):
        self.cache_manager = CacheManager(cache_file)
    
    def __str__(self):
        return f"GoogleSerper(cache_file='{self.cache_manager.cache_file}')"
    
    def __repr__(self):
        return f"<GoogleSerper cache_file='{self.cache_manager.cache_file}'>"

    def google_serper(self, query):
        cache = self.cache_manager.get_cache()
        if query in cache:
            return cache[query]
        response = GoogleSerperAPIWrapper().run(query)
        self.cache_manager.update_cache(query, response)
        return response
