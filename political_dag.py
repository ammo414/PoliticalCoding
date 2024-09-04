from datetime import datetime
from airflow.decorators import dag, task

import billCoding
import newsCoding

"""
example of airflow dag to ingest data daily
"""

@dag(schedule='@daily', start_date=datetime(2021, 12, 1), catchup=False)
def taskflow():
    @task(task_id='get_bills')
    def billsAirflow():
        try:
            billCoding.get_bills()
        except:
            return False

    @task(task_id='get_news')
    def newsAirflow():
        try:
            newsCoding.get_news()
        except:
            return False

    @task(task_id='political_data_ingest')
    def political_data_ingest(a, b):
        if a and b:
            print('works')
        else:
            print('doesn\'t')

    a = billsAirflow()
    b = newsAirflow()
    political_data_ingest(a, b)

taskflow()
