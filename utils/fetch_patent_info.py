# File: patent_info_manager.py

import os
import requests
import xmltodict
from utils.cache_manager import CacheManager

from dotenv import load_dotenv

load_dotenv()

class FetchPatentInfo:
    def __init__(self, cache_file="response_cache/response_cache_patent.pkl"):
        """
        Initialize the PatentInfoManager with a cache file.
        """
        self.cache_manager = CacheManager(cache_file)
    
    def fetch_patent_info(self, keyword):
        """
        Fetch patent information using KIPRIS API with caching for results.
        
        Args:
            keyword (str): The keyword to search for.
        
        Returns:
            str: Patent information context in Korean.
        """
        # Check if the keyword is already in the cache
        cache = self.cache_manager.get_cache()
        if keyword in cache:
            return cache[keyword]

        # API base URL and key
        base_url = "http://plus.kipris.or.kr/openapi/rest/patUtiModInfoSearchSevice/freeSearchInfo"
        api_key = os.getenv("KIPRIS_REST_KEY").replace("\"", "")
        query_url = f"{base_url}?word={keyword}&docsStart=1&docsCount=3&lastvalue=R&accessKey={api_key}"

        try:
            response = requests.get(query_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error occurred during API request: {e}")
            return []

        # Parse the XML response
        content = response.content
        dict_type = xmltodict.parse(content)
        try:
            PatentInfo = dict_type['response']['body']['items']['PatentUtilityInfo']
        except KeyError:
            PatentInfo = ""

        # Map keys to Korean context
        key_mapping = {
            'Applicant': '출원인',
            'ApplicationNumber': '출원번호',
            'InventionName': '특허명',
            'Abstract': '초록',
            'RegistrationStatus': '등록상태'
        }
        context = str([{new_key: item[old_key] for old_key, new_key in key_mapping.items() if old_key in item} for item in PatentInfo])

        # Cache the result
        self.cache_manager.update_cache(keyword, context)
        
        return context
