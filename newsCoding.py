import constants

import utils.project_utils as utils
import utils.llm_utils as llm_utils
import article_objects

"""
all news processing
"""

def get_news():
    """
    main function. creates csv, unpacks and processes JSON, writes data to csv"""
    news_api_key = constants.PERIGON_API_KEY

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
        news_code = cap_code(news_article)
        news_article.add_cap_code(news_code)

        news_article.write_to_csv(filename)


def cap_code(news_article: article_objects.News):
    """
    uses an LLM to find the best cap_code
    """
    
    cap_code_crossmap = {'macroeconomics':1,
                        'civil rights':2,
                        'health':3,
                        'agriculture':4,
                        'labor':5,
                        'education':6,
                        'environment':7,
                        'energy':8,
                        'immigration':9,
                        'transportation':10,
                        'law and crime':12,
                        'social welfare':13,
                        'housing':14,
                        'domestic commerce':15,
                        'defense':16,
                        'technology':17,
                        'foreign trade':18,
                        'international affairs':19,
                        'government operations':20,
                        'public lands':21,
                        'culture':23,
                        '0': 0
                        }
    
    message_str = llm_utils.send_to_open_ai(news_article)

    code = 0
    try:
        code = cap_code_crossmap[message_str]
    except KeyError:
        print('Invalid response from LLM')

    return code


if __name__ == '__newsCoding__':
    get_news()