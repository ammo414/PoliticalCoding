import newsCoding
import billCoding

import utils.project_utils as utils


if __name__ == '__main__':
    #Archive data from previous runs
    utils.move_csvs_to_archive('bills')
    utils.move_csvs_to_archive('news')

    billCoding.get_bills()
    newsCoding.get_news_google_rss()
