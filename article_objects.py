import csv

import uitls.constants
from utils.db_utils import PostGreManager as pgm


class Article:
    """
    Barebone description of either a Bill or News Article
    """

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
        try:
            return self.title
        except AttributeError as error:
            print(error)
            return None

    def write_to_csv(self,filename) -> None:
        row = vars(self).keys()
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter='|')
            writer.writerow(row)        

    def send_query(self):
        db = pgm(constants.db_config)
        placeholders = vars(self)

        if isinstance(self, News):
            if len(placeholders) == 6:
                return db.execute_query('INSERT INTO {} VALUES (%s, %s, %s, %s, %s, %s)', 'news', placeholders.values())
            
            else:
                print(f'Row length mishap. Look at {self.article_id} for more info')
                return False
            
        elif isinstance(self, Bill):
            if len(placeholders) == 7:
                return db.execute_query('INSERT INTO {} VALUES (%s, %s, %s, %s, %s, %s, %s)', 'bill', placeholders.values())
            
            else:
                print(f'Row length mishap. Look at {self.number} for more info')
                return False
        
        else:
            print(f"Article {self.title} is neither News or Bill. Check call")
            return False


class News(Article):
    """ 
    adds news specific attributes and method
    """
    def __init__(self, article_id, url, source, pub_date, title, description):
        Article.__init__(self, article_id, url, source, pub_date, title, description)
        self.article_id: int = article_id
        self.source: str = source
        self.pub_date: str = pub_date
        self.description: str = description
    
    def get_description(self) -> str:
        try:
            return self.description # might be None...
        except AttributeError as error:
            return self.title


class Bill(Article):
    """
    adds bill specific attributes and methods
    """
    def __init__(self, number, title, url, committees, policy_area, type, congress):
        Article.__init__(self, number, title, url, committees, policy_area, bill_type, congress)
        self.number: int = number
        self.committees: list = committees
        self.policy_area: str = policy_area
        self.type: str = bill_type
        self.congress: int = congress

    def get_committees(self):
        try:
            return self.committees
        except AttributeError as error:
            print(error)
            return None
        
    def get_policy_area(self):
        try:
            return self.policy_area
        except AttributeError as error:
            print(error)
            return None