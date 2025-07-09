import os
import requests
import nltk
import yake
from abc import ABC, abstractmethod

# Download required NLTK data
try:
    nltk.data.find('stopwords')
except LookupError:
    nltk.download('stopwords')
    nltk.download('punkt')

class KeywordExtractor(ABC):
    @abstractmethod
    def extract_keywords(self, text, num_keywords=5):
        pass

class YakeKeywordExtractor(KeywordExtractor):
    def __init__(self):
        self.yake = yake.KeywordExtractor(
            lan="en",
            n=3,  # max n-gram size
            dedupLim=0.7,
            dedupFunc='seqm',
            windowsSize=1,
            top=20
        )
        
    def extract_keywords(self, text, num_keywords=5):
        """Extract keywords using YAKE algorithm"""
        keywords = self.yake.extract_keywords(text)
        
        # Extract only the phrases (not scores)
        result = []
        for kw, score in keywords[:num_keywords]:
            # Add individual words from multi-word phrases
            words = kw.split()
            result.extend(words)
            
        # Remove duplicates
        seen = set()
        unique_keywords = []
        for kw in result:
            if kw.lower() not in seen:
                seen.add(kw.lower())
                unique_keywords.append(kw)
                
        return unique_keywords[:num_keywords]

class KeywordExtractorFactory:
    @staticmethod
    def create_extractor(method="rake", api_key=None):
        """Factory method to create appropriate keyword extractor"""
        if method == "cortical" and api_key:
            return CorticalKeywordExtractor(api_key)
        elif method == "yake":
            return YakeKeywordExtractor()
        # else:
        #     return RakeKeywordExtractor()