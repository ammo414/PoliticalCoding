"""common functions for the rest of the project"""

import shutil
from pathlib import Path
from datetime import datetime
import time
import xml.etree.ElementTree as ET

import requests


def load_json(url, which_data):
    """loads json and returns content"""

    time.sleep(1)
    response = requests.get(url, timeout=5)
    content = response.json()

    if which_data == 'bill':
        if 'error' in content:
            print(content['error'])
            return None
        content_type = content['request']['format']
        if content_type != 'json':
            print(f'{content_type} content type. You\'ll need to fix that.')
            return None

    # not currently using json for news, but space is here if things change

    return content


def load_rss(url):
    """loads rss into an xlm tree"""
    time.sleep(1)
    response = requests.get(url, timeout=1)
    rss_feed = ET.fromstring(response.text)

    return rss_feed


def move_csvs_to_archive(which_data):
    """if csvs are in present directory, moves them to an archive dir"""
    source_dir = Path()
    archive_dir = Path('./archive')

    archive_dir.mkdir(parents=True, exist_ok=True)

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
