"""main"""
import news_coding
import bill_coding
from utils import project_utils as utils, db_utils, constants


if __name__ == '__main__':
    #archive data from previous runs
    utils.move_csvs_to_archive('bill')
    utils.move_csvs_to_archive('news')

    #create tables in database if not already present
    db = db_utils.PostGreManager(constants.db_config)
    db.connect()
    db.create_table_if_not_exist('bill')
    db.create_table_if_not_exist('news')
    db.close()

    #do the data
    bill_coding.get_bills()
    news_coding.get_news_google_rss()
