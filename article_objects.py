import csv

class Article:
    """
    Barebone describes either a Bill or News Article
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
        except AttributeError:
            return None

    def write_to_csv(self, filename):
        row = [self.number, self.title, self.url, self.committees, self.policy_area, self.type, self.congress, self.cap_code]
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter='|')
            writer.writerow(row)


class News(Article):
    def __init__(self, article_id, url, source, pub_date, title, description):
        Article.__init__(self, article_id, url, source, pub_date, title, description)
        self.article_id: int = article_id
        self.source: str = source
        self.pub_date: str = pub_date
        self.description: str = description
    
    def get_description(self) -> str:
        return self.description
    

class Bill(Article):
    def __init__(self, number, title, url, committees, policy_area, type, congress):
        Article.__init__(self, number, title, url, committees, policy_area, type, congress)
        self.number: int = number
        self.committees: list = committees
        self.policy_area: str = policy_area
        self.type: str = type
        self.congress: int = congress

    def get_committees(self):
        try:
            return self.committees
        except AttributeError:
            return None
        
    def get_policy_area(self):
        try:
            return self.policy_area
        except AttributeError:
            return None
        
    