"""main"""
import news_coding
import bill_coding
from utils import project_utils as utils


if __name__ == '__main__':
    #Archive data from previous runs
    utils.move_csvs_to_archive('bill')
    utils.move_csvs_to_archive('news')

    #bill_coding.get_bills()
    news_coding.get_news_google_rss()
