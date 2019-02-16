#
# Package ArticleScraper
#

# https://realpython.com/python-requests/
import requests as _requests
import TextHelper.TextHelper as TextHelper
from lxml import etree as ElemTree, html as LHtml
from datetime import datetime as DateTime, timedelta as TimeDelta
from Article.Article import Article
from NLPHelper.NLPHelper import NLPHelper
from builtins import int
import operator as Operator

# https://docs.python.org/3.7/library/xml.etree.elementtree.html
import xml.etree.ElementTree as _ElementTree


class ArticleScrapper:
    
    def __init__(self):
        self.sources_information = None
        self.number_of_articles = 0
        self.article_list = {}
        self.similarity_matrix = {}
        self.nlp_helper = NLPHelper()

    def add_article(self, article_information):
        # Checking whether the article already exists
        for article in list(self.article_list.values()):
            if (
                (article_information['source'])
                and (article_information['title'])
                and (article_information['source'] == article.source)
                and (article_information['title'] == article.title)
            ):
                return True
        
        if self.nlp_helper and 'content' in article_information:
            article_information['nlp_clean_content'] = self.nlp_helper.clean_raw_text(article_information['content'])
        
        self.article_list[self.number_of_articles] = Article(article_information)
        self.number_of_articles = self.number_of_articles + 1
        
        return

    def load_articles(self, sources_information):
        self.sources_information = sources_information
        
        # Iterating through each feed source
        for source_key, source_data in self.sources_information.items():
        
            # Iterating through each feed_url
            for feed_url in source_data['feeds']:
                # feeds_xml = _requests.get(feed_url)
                # xml_tree = _ElementTree.fromstring(feeds_xml.text)

                xml_tree = _ElementTree.parse(feed_url)
                
                # TODO: Move this to an external function/class
                # Huffington Post
                if source_key == 'huffingtonpost':
                    print("Aqui 2")
                    feed_items = xml_tree.findall('.//channel/item')
                    
                    for item in feed_items:
                        # Check the date
                        # article_date = DateTime.strptime(item.findall('pubDate/text()')[0], '%a, %d %b %Y %H:%M:%S %z').astimezone()
                        # if (DateTime.now().astimezone() - article_date) > TimeDelta(days=1):
                            # continue

                        print("Aqui 3")
                        
                        # Check the categories
                        article_categories = item.findall('category')
                        for category in article_categories:
                            print(category.text)

                        exit()


                        article_categories = item.xpath('category/text()')
                        if not (set(source_data['allowed_categories']) & set(article_categories)):
                            continue

                        print("Aqui 4")
                        
                        # Adding the new article
                        self.add_article({
                            'title': item.xpath('title/text()')[0],
                            'content': TextHelper.clean_html(item.xpath('description/text()')[0]),
                            'date': article_date,
                            'categories': article_categories,
                            'link': item.xpath('link/text()')[0],
                            'source': 'huffingtonpost',
                            'base_score': 1
                        })
                
                # Publico
                elif source_key == 'publico':
                    feed_items = xml_tree.xpath('//channel/item')
                    
                    for item in feed_items:
                        # Check the date
                        article_date = DateTime.strptime(item.xpath('pubDate/text()')[0], '%a, %d %b %Y %H:%M:%S %z').astimezone()
                        if (DateTime.now().astimezone() - article_date) > TimeDelta(days=1):
                            continue
                        
                        # Check the categories
                        article_categories = item.xpath('category/text()')
                        if not (set(source_data['allowed_categories']) & set(article_categories)):
                            continue
                        
                        # To get the content, we need to follow the article link
                        article_html_page = Requests.get(item.xpath('link/text()')[0])
                        article_dom_tree = LHtml.fromstring(article_html_page.content)
                        article_raw_content = article_dom_tree.xpath('//div[contains(@class, "article-text")]')[0]
                        article_html_content = ElemTree.tostring(article_raw_content).decode('utf-8')
                        
                        # Adding the new article
                        self.add_article({
                            'title': item.xpath('title/text()')[0],
                            'subtitle': TextHelper.clean_html(item.xpath('description/text()')[0]),
                            'content': TextHelper.clean_html(article_html_content),
                            'date': article_date,
                            'categories': article_categories,
                            'link': item.xpath('link/text()')[0],
                            'source': 'publico',
                            'base_score': 1
                        })
                            
                # El Pais
                elif source_key == 'elpais':
                    feed_items = xml_tree.xpath('//channel/item')
                    
                    for item in feed_items:
                        # Check the date
                        # Tue, 20 Jun 2017 14:16:41 +0200
                        article_date = DateTime.strptime(item.xpath('pubDate/text()')[0], '%a, %d %b %Y %H:%M:%S %z').astimezone()
                        if (DateTime.now().astimezone() - article_date) > TimeDelta(days=1):
                            continue
                    
                        # Check the categories
                        article_categories = item.xpath('category/text()')
                        if not (set(source_data['allowed_categories']) & set(article_categories)):
                            continue
                        
                        # To get the content, we need to follow the article link
                        article_html_page = Requests.get(item.xpath('link/text()')[0])
                        article_dom_tree = LHtml.fromstring(article_html_page.content)
                        article_raw_content = article_dom_tree.xpath('//div[contains(@class, "articulo-cuerpo")]')
                        if article_raw_content:
                            article_raw_content = article_raw_content[0]
                            for extra_content in article_raw_content.xpath('//section[contains(@class, "sumario_apoyos")]'):
                                extra_content.getparent().remove(extra_content)
        
                            article_html_content = ElemTree.tostring(article_raw_content).decode('utf-8')
                        else:
                            article_html_content = item.xpath('description/text()')[0]
                            
                        # Adding the new article
                        self.add_article({
                            'title': item.xpath('title/text()')[0],
                            'subtitle': TextHelper.clean_html(item.xpath('description/text()')[0]),
                            'content': TextHelper.clean_html(article_html_content),
                            'date': article_date,
                            'categories': article_categories,
                            'link': item.xpath('link/text()')[0],
                            'source': 'elpais',
                            'base_score': 1
                        })
        return
    
    def calculate_similarity(self):
        if not self.article_list: 
            return False
        
        if not self.nlp_helper:
            return False
        
        for news_article_id, news_article in self.article_list.items():
            for other_news_article_id, other_news_article in self.article_list.items():
                news_article_id = str(news_article_id)
                other_news_article_id = str(other_news_article_id)
                
                if news_article_id == other_news_article_id:
                    continue
                
                if (
                    (news_article_id in self.similarity_matrix and other_news_article_id in self.similarity_matrix[news_article_id])
                    or (other_news_article_id in self.similarity_matrix and news_article_id in self.similarity_matrix[other_news_article_id])
                ):
                    continue
                
                if news_article_id not in self.similarity_matrix:
                    self.similarity_matrix[news_article_id] = {}
                    
                if other_news_article_id not in self.similarity_matrix:
                    self.similarity_matrix[other_news_article_id] = {}
                    
                news_article_clean_content = news_article.get_clean_content()
                other_news_article_clean_content = other_news_article.get_clean_content()
                similarity_score = self.nlp_helper.calculate_similarity_score(news_article_clean_content, other_news_article_clean_content) * 100
                
                if self.nlp_helper.get_text_richness(news_article_clean_content) >= self.nlp_helper.get_text_richness(other_news_article_clean_content) :
                    self.similarity_matrix[news_article_id][other_news_article_id] = similarity_score
                    self.similarity_matrix[other_news_article_id][news_article_id] = (similarity_score * -1)
                    news_article.add_similarity_score(similarity_score)
                    other_news_article.add_similarity_score(similarity_score * -1)
                    
                else:
                    self.similarity_matrix[news_article_id][other_news_article_id] = (similarity_score * -1)
                    self.similarity_matrix[other_news_article_id][news_article_id] = similarity_score
                    news_article.add_similarity_score(similarity_score * -1)
                    other_news_article.add_similarity_score(similarity_score)
                
                # Debugging
                # print ("Score article " + news_article_id + " - " + other_news_article_id + " => " + str(self.similarity_matrix[news_article_id][other_news_article_id]))
        return self.similarity_matrix

    def get_sorted_articles(self, limit=10):
        if not self.article_list:
            return False
        
        sorted_articles = {}
        for article_id, article in self.article_list.items():
            sorted_articles[article_id] = article.get_score()
            
        sorted_articles = sorted(sorted_articles.items(), key=Operator.itemgetter(1), reverse=True)
        return sorted_articles[:limit]

    def print_article(self, article_id):
        article_id = int(article_id)
        
        if not article_id in list(self.article_list.keys()):
            return False
        
        return self.article_list[article_id].print()

    def get_articles(self):
        return self.article_listload_articles
