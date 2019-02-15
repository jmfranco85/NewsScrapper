
from spacy.es import Spanish


class SpacyHelper:
    
    def __init__(self):
        self.nlp = Spanish()
        
    # Removes stop_words and stems
    def clean_raw_text(self, text):
        return text

    def get_text_richness(self, clean_text):
        return len(set(clean_text))
    
    def calculate_similarity_score(self, text1, text2):
        if not self.nlp:
            return False
        
        text1_nlp = self.nlp(text1)
        text2_nlp = self.nlp(text2)
        return text1_nlp.similarity(text2_nlp)
