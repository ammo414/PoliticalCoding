"""
create new column for introduced_date for bills table 
and then backfill data
"""

from utils import project_utils as utils, constants
from utils.db_utils import PostGreManager as pgm


def new_column():
    """statement to add bill column"""
    new_column_statement = (
        "ALTER TABLE {}"
        "ADD COLUMN IF NOT EXISTS introduced_date date"
    )
    table = "bill"
    return new_column_statement, table


def return_bill_urls():
    """statement to select column of urls"""
    select_bill_url = "SELECT number, url FROM {} WHERE introduced_date is NULL"
    table = "bill"
    params = ("number", "url", "introduced_date")
    return select_bill_url, table, params


def get_introduced_date(url_column):
    """query url and return introduced_date"""
    ret = {}  # number : introduced_date
    congress_api_key = constants.CONGRESS_API_KEY
    for r in url_column:
        url = r[1] + '?api_key=' + congress_api_key
        content = utils.load_json(url, "bill")
        introduced_date = content['bill']['introducedDate']
        ret[r[0]] = introduced_date
    return ret


if __name__ == "__main__":
    db = pgm(constants.db_config)
    if db.connect():
        nc = new_column()
        db.exec_query(nc[0], nc[1])
        rbu = return_bill_urls()
        bill_url = db.exec_query(rbu[0], rbu[1]) #, rbu[2])
        ids_and_dates = get_introduced_date(bill_url)
        for number, date in ids_and_dates.items():
            db.exec_query((
                "UPDATE {}"
                "SET introduced_date = %s"
                "WHERE number = %s"
            ), "bill", (date, number))
