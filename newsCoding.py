import xml.etree as ET

import constants
import utils.project_utils as utils
import utils.llm_utils as llm_utils
from utils.db_utils import PostGreManager as pgm
import article_objects


"""
all news processing
"""

def get_news_perignon():
    """
    main function. creates csv, unpacks and processes JSON, writes data to csv
    """
    
    news_api_key = constants.PERIGON_API_KEY
    
    db = pgm(constants.db_config)
    db.connect()

    url = f'https://api.goperigon.com/v1/all?apiKey={news_api_key}&from=2024-07-26&country=us&sourceGroup=top100&showNumResults=true&showReprints=false&excludeLabel=Non-news&excludeLabel=Opinion&excludeLabel=Paid%20News&excludeLabel=Roundup&excludeLabel=Press%20Release&sortBy=date&language=en&category=Politics'
    content = utils.load_url(url, 'news')

    filename = utils.get_filename('news')

    for n in content['articles']:
        news_article_id = n['articleId']
        news_url = n['url']
        news_source = n['source']['domain']
        news_pub_date = n['pubDate']
        news_title = n['title']
        news_description = n['description']

        news_article = article_objects.News(news_article_id, news_url, news_source, news_pub_date, news_title, news_description)
        #news_code = cap_code(news_article)
        news_article.add_cap_code(-1)

        news_article.write_to_csv(filename)
        placeholders = vars(news_article)
    
        news_article.send_query()
        

def load_google_rss(url):
    response = requests.get(url)
    rss_feed = ET.fromstring(url)
    
    return rss_feed

def get_news_google_rss():

    url = 'https://rss.app/feeds/IbzouYj7CpKSEWRi.xml'
    rss_feed = load_google_rss(url)

    filename = utils.get_filename('news')

    for item in rss_feed.iter('item'):
        news_article_id = item.find('guid').text
        news_url = item.find('link').text
        news_source = news_url.split('.com')[0][8:] #everything before ".com" and after "https://"
        news_pub_date = item.find('pubDate').text
        news_title = item.find('title').text
        news_description = item.find('description').text

        news_article = article_objects.News(news_article, news_url, news_source, news_pub_date, news_title, news_description)
        news_code = cap_code(news_article)
        news_article.add_cap_code(news_code) # don't use perplexity. Use huggingface instead

        news_article.wite_to_csv(filename)
        news_article.send_query()


def cap_code(news_article: article_objects.News):
    """
    uses an LLM to find the best cap_code
    """
    
    news_text = '|'.join((news_article.get_title, news_article.get_description))
    llm_utils.classify_text_with_huggingface(news_text, news)

    # perplexity approach. too (monetarily) costly
    # message_str = llm_utils.send_to_open_ai(news_article)

    return code


if __name__ == '__newsCoding__':
    #get_news_perignon()
    get_news_google_rss()