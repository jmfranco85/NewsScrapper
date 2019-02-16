#
# News Scraper
#

"""
Next steps:
    - Every article must have a score calculated when adding a new Article to the ArticleScraper
    - Feed sources must be different classes as per the source
    - Add new languages to the NLP Helpers
    - Use the NLP_METHODS constant and instantiate the class with the "classname" property in the NLPHelper class
    - Treat the texts separately so when calculating the sets we have the stop_words and the stems removed (In the NLP helpers)
    - Add Log system
"""

from Article.ArticleScrapper import ArticleScrapper
import json as _json

final_list_of_news = {}

"""
##########
## MAIN ##
##########
"""

if __name__ == "__main__":
    print("---------------------------------------");
    print("--          Article Scraper          --");
    print("---------------------------------------");

    a_scraper = ArticleScrapper()

    # Loading articles from the sources
    news_sources = _json.load(open('sources.json'))
    a_scraper.load_articles(news_sources)
	
	# Test conflict

    exit()

    # Calculating the similarity scores
    a_scraper.calculate_similarity()

    # Getting the last articles by score
    news_articles = a_scraper.get_sorted_articles()
    if not news_articles:
        print(" NO FINAL LIST OF NEWS ")
        exit()

    # Printing articles
    for news_article_item in news_articles:
        news_article_id = news_article_item[0]
        news_article_score = news_article_item[1]

        news_article_content = a_scraper.print_article(news_article_id)
        if not news_article_content:
            continue

        print("---------------------------------\n")
        print(str(news_article_id) + " - " + news_article_content)
        print("---------------------------------\n")

    print(" THE END! ")
