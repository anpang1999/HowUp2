import os
import pickle

class CacheManager:
    def __init__(self, cache_file_path):
        """
        Initialize the CacheManager with the given cache file path.
        If the cache file exists, load its contents; otherwise, initialize an empty dictionary.
        """
        self.cache_file_path = cache_file_path
        if os.path.exists(self.cache_file_path):
            with open(self.cache_file_path, "rb") as f:
                self.cache_data = pickle.load(f)
        else:
            self.cache_data = {}
            self.save_cache()  # Save an empty cache initially

    def save_cache(self):
        """
        Save the current cache data to the file.
        """
        with open(self.cache_file_path, "wb") as f:
            pickle.dump(self.cache_data, f)

    def get_cache(self):
        """
        Get the current cache data.
        """
        return self.cache_data

    def update_cache(self, key, value):
        """
        Update the cache with a new key-value pair and save it.
        """
        self.cache_data[key] = value
        self.save_cache()

    def clear_cache(self):
        """
        Clear the cache data and save an empty dictionary.
        """
        self.cache_data = {}
        self.save_cache()


# Example usage:
CACHE_FILE_PATENT = "response_cache/response_cache_patent.pkl"
CACHE_FILE_SERP = "response_cache/response_cache_serp.pkl"

# Create CacheManager instances
patent_cache = CacheManager(CACHE_FILE_PATENT)
serp_cache = CacheManager(CACHE_FILE_SERP)

# Example operations
patent_cache.update_cache("example_key", "example_value")
serp_cache.update_cache("search_query", "search_results")

print(patent_cache.get_cache())
print(serp_cache.get_cache())
