"""all news processing"""

import xml.etree.ElementTree as ET

from utils import llm_utils, project_utils as utils
import article_objects


def create_news_table():
    """returns statements to check if 'news' table exists and, if not, creates it"""
    statement = (
        "CREATE TABLE IF NOT EXISTS {}"
        "("
        "title text not null,"
        "url text not null,"
        "cap_code text,"
        "article_id text primary key,"
        "source text,"
        "pub_date timestamp with time zone,"
        "description text"
        ");"
    )
    table = "news"
    return statement, table


def get_news_google_rss():
    """get news from google news' rss feed"""

    url = "https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US%3Aen&oc=11&q=politics"
    rss_feed: ET = utils.load_rss(url)

    filename = utils.get_filename("news")

    for item in rss_feed.iter("item"):
        news_article_id = item.find("guid").text
        news_url = item.find("link").text
        news_title = item.find("title").text
        news_source = news_title.split(' - ')[-1]
        news_pub_date = item.find("pubDate").text
        news_description = news_title  # google news doesn't have any additional info

        news = article_objects.News(
            news_article_id,
            news_url,
            news_source,
            news_pub_date,
            news_title,
            news_description,
        )

        if not news.in_table():
            news_code = cap_code(news)
            news.add_cap_code(news_code)

            news.print_row()
            news.write_to_csv(filename)
            news.insert_into_sql()


def cap_code(news_article: article_objects.News):
    """
    uses an LLM to find the best cap_code
    """

    news_text = "|".join((news_article.get_title(), news_article.get_description()))
    return llm_utils.classify_text_with_huggingface(news_text, "news")


if __name__ == "__news_coding__":
    get_news_google_rss()
