import shutil
from pathlib import Path
from datetime import datetime
import requests
import time
import xml.etree.ElementTree as ET


"""
common functions for the rest of the project
"""

def load_url(url, type):
    """
    loads url and returns content
    """
    
    time.sleep(1)
    response = requests.get(url)
    content = response.json()

    if type == 'bill':
        if 'error' in content:
            print(content['error'])
            return None
        content_type = content['request']['format']
        if content_type != 'json':
            print(f'{content_type} content type. You\'ll need to fix that.')
            return None
    
    elif type == 'news':
        pass # haven't seen any errors yet

    return content


def move_csvs_to_archive(which_data):
    source_dir = Path()
    archive_dir = Path('./archive')

    for file_path in source_dir.iterdir():
        if str(file_path).endswith(".csv") and which_data in str(file_path):
            shutil.move(str(file_path), str(archive_dir)+'/'+str(file_path))
    

def get_filename(which_data):
    """
    creates filename for csvs for both bills and news
    which_data should be either 'bill' or 'news'
    """
    now = datetime.now().strftime('%d-%m-%y|%H:%M')
    filename = f'{which_data}|{now}.csv'
    return filename