"""Classes to describe News or Bill articles."""

import csv

from utils import constants
from utils.db_utils import PostGreManager as pgm


class Article:
    """Barebone description of either a Bill or News Article"""

    def __init__(self, title, url):
        self.title: str = title
        self.url: str = url
        self.cap_code = 0

    def add_cap_code(self, cap_code: int) -> None:
        """
        adds CAP code
        See https://www.comparativeagendas.net/pages/master-codebook
        for more details.
        """

        self.cap_code = cap_code

    def get_title(self):
        """gets title or None"""
        try:
            return self.title
        except AttributeError as error:
            print(error)
            return None

    def write_to_csv(self, filename) -> None:
        """appends row to csv"""
        row = vars(self).values()
        with open(filename, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter="^")
            writer.writerow(row)

    def print_row(self):
        """prints values for debugging"""
        print(vars(self).values())

    def insert_into_sql(self):
        """sends an INSERT statement to the database"""
        db = pgm(constants.db_config)
        placeholders = vars(self)
        print(placeholders)
        db.connect()
        try:
            if isinstance(self, News):
                if len(placeholders) == 7:
                    return db.exec_query(
                        "INSERT INTO {} VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        "news",
                        tuple(placeholders.values()),
                    )

                else:
                    print(f"Row length mishap. Look at {self.article_id} for more info")
                    return False

            elif isinstance(self, Bill):
                if len(placeholders) == 8:
                    return db.exec_query(
                        "INSERT INTO {} VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        "bill",
                        tuple(placeholders.values()),
                    )

                else:
                    print(f"Row length mishap. Look at {self.number} for more info")
                    return False

            else:
                print(f"Article {self.title} is neither News or Bill. Check call")
                return False
        finally:
            db.close()


class News(Article):
    """
    adds news specific attributes and method
    """

    def __init__(self, article_id, url, source, pub_date, title, description):
        Article.__init__(self, title, url)
        self.article_id: int = article_id
        self.source: str = source
        self.pub_date: str = pub_date
        self.description: str = description

    def get_description(self) -> str:
        """gets description"""
        try:
            return self.description  # might be None...
        except AttributeError as error:
            print(error)
            return self.get_title()


class Bill(Article):
    """
    adds bill specific attributes and methods
    """

    def __init__(
        self, number, title, url, committees, policy_area, bill_type, congress
    ):
        Article.__init__(self, title, url)
        self.number: int = number
        self.committees: list = committees
        self.policy_area: str = policy_area
        self.bill_type: str = bill_type
        self.congress: int = congress

    def get_committees(self):
        """gets committees"""
        try:
            return self.committees
        except AttributeError as error:
            print(error)
            return None

    def get_policy_area(self):
        """gets policy area"""
        try:
            return self.policy_area
        except AttributeError as error:
            print(error)
            return None
