#
# Class Article
#


class Article:
    
    def __init__(self, article_information):
        self.title = None
        self.subtitle = None
        self.content = None
        self.nlp_clean_content = None
        self.date = None
        self.categories = []
        self.link = None
        self.source = None
        self.base_score = 0
        self.similarity_score = {
            'count': 0,
            'min': 0,
            'max': 0,
            'total': 0,
            'average': 0
        }
        
        if 'title' in article_information:
            self.title = article_information['title']
        if 'subtitle' in article_information:
            self.subtitle = article_information['subtitle']
        if 'content' in article_information:
            self.content = article_information['content']
        if 'nlp_clean_content' in article_information:
            self.nlp_clean_content = article_information['nlp_clean_content']
        if 'date' in article_information:
            self.date = article_information['date']
        if 'categories' in article_information:
            self.categories = article_information['categories']
        if 'link' in article_information:
            self.link = article_information['link']
        if 'source' in article_information:
            self.source = article_information['source']
        if 'base_score' in article_information:
            self.base_score = article_information['base_score']

    def get_clean_content(self):
        if self.nlp_clean_content:
            return self.nlp_clean_content
        
        return self.content
    
    def add_similarity_score(self, similarity_score):
        self.similarity_score['total'] = self.similarity_score['total'] + similarity_score
        self.similarity_score['count'] = self.similarity_score['count'] + 1
        self.similarity_score['average'] = self.similarity_score['total'] / self.similarity_score['count']
        
        if similarity_score > self.similarity_score['max']:
            self.similarity_score['max'] = similarity_score
            
        if similarity_score < self.similarity_score['min']:
            self.similarity_score['min'] = similarity_score
        
    # TODO: Add different score valuations
    def get_score(self):
        return self.similarity_score['average']
    
    def print(self):
        article_str = ""
        article_str += self.title + "\n"
        if self.content:
            article_str += self.content + "\n"
        article_str += "Fecha: " + str(self.date) + "\n"
        article_str += "Categorías: " + ', '.join(self.categories) + "\n"
        article_str += "Enlace: " + self.link + "\n"
        article_str += "Puntuación: " + str(self.get_score()) + "\n"
            
        return article_str
