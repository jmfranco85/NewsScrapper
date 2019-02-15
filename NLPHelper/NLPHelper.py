
from NLPHelper.NLTKHelper import NLTKHelper
from NLPHelper.SpacyHelper import SpacyHelper

#
# Constants
#
"""
NLP_METHODS = {
    'NLP_METHOD_NLTK': {
        'classname': 'NLTKHelper'
    },
   'NLP_METHOD_SPACY': {
       'classname': 'SpacyHelper'
   }
}
"""

NLP_METHOD_NLTK = 'NLP_METHOD_NLTK'
NLP_METHOD_SPACY = 'NLP_METHOD_SPACY'
NLP_ALLOWED_METHODS = [NLP_METHOD_NLTK, NLP_METHOD_SPACY]


class NLPHelper:
    
    def __init__(self, nlp_method=NLP_METHOD_NLTK):
        # TODO: throw exception here
        if nlp_method not in NLP_ALLOWED_METHODS:
            return None
        
        if nlp_method == NLP_METHOD_NLTK:
            self.nlp_handler = NLTKHelper()
        elif nlp_method == NLP_METHOD_SPACY:
            self.nlp_handler = SpacyHelper()
        else:
            self.nlp_handler = None
    
    # Removes stop_words and stems
    def clean_raw_text(self, text):
        if not self.nlp_handler:
            return False
        
        return self.nlp_handler.clean_raw_text(text)
    
    def calculate_similarity_score(self, text1, text2):
        if not self.nlp_handler:
            return False
        
        return self.nlp_handler.calculate_similarity_score(text1, text2)
    
    def get_text_richness(self, text):
        if not self.nlp_handler:
            return False
        
        return self.nlp_handler.get_text_richness(text)
