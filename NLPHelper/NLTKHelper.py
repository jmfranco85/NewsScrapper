
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

# Global parameters
stemmer = nltk.stem.snowball.SpanishStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
spanish_stop_words_list = [word for word in stopwords.words('spanish')]


def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]


def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))


class NLTKHelper:
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words=spanish_stop_words_list)

    # Removes stop_words and stems
    def clean_raw_text(self, text):
        return text

    def get_text_richness(self, clean_text):
        return len(set(clean_text))
    
    # Text should be cleaned already
    def calculate_similarity_score(self, clean_text1, clean_text2):
        if not self.vectorizer:
            return False
        
        ################
        # Stem and Stop words comparison (Get the stems and removes the stop words from the texts and compares them)
        tfidf = self.vectorizer.fit_transform([clean_text1, clean_text2])
        similarity_score = (tfidf * tfidf.T).A[0, 1]
        return similarity_score
