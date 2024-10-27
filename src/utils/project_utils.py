"""common functions for the rest of the project"""

import shutil
from pathlib import Path
from datetime import datetime
import time
import xml.etree.ElementTree as ET
from getpass import getpass

import requests


def load_json(url, which_data):
    """loads json and returns content"""

    time.sleep(1)
    response = requests.get(url, timeout=5)
    content = response.json()

    if which_data == "bill":
        if "error" in content:
            print(content["error"])
            return None
        content_type = content["request"]["format"]
        if content_type != "json":
            print(f"{content_type} content type. You'll need to fix that.")
            return None

    # not currently using json for news, but space is here if things change

    return content


def load_rss(url):
    """loads rss into an xlm tree"""
    time.sleep(1)
    response = requests.get(url, timeout=1)
    rss_feed = ET.fromstring(response.text)

    return rss_feed


def create_constants():
    """Create ./src/utils/constants.py file if not exists and asks for secrets"""
    constants_file: Path = Path("./src/utils/constants.py")
    print(constants_file)

    if not constants_file.is_file():
        print("HELLOOOOO")
        ask_for_secrets = input("Do you want to add constants now? (y/n): ")
        if ask_for_secrets.lower() == "y":
            host = input("Host Name?: ")
            dbname = input("Database Name?: ")
            user = input("User Name?: ")
            password = getpass("Password?: ")
            congress_api_key = getpass("Congress API Key?: ")
        else:
            host = ""
            dbname = ""
            user = ""
            password = ""
            congress_api_key = ""

        file_lines = [None] * 10
        file_lines[0] = '"""Globcal config constants for use in the entire project"""'
        file_lines[1] = ""
        file_lines[2] = "db_config = {"
        file_lines[3] = f'\t"HOST": "{host}"'
        file_lines[4] = f'\t"DBNAME": "{dbname}"'
        file_lines[5] = f'\t"USER": "{user}"'
        file_lines[6] = f'\t"PASSWORD": "{password}"'
        file_lines[7] = "}"
        file_lines[8] = ""
        file_lines[9] = f"CONGRESS_API_KEY = {congress_api_key}"

        with open(str(constants_file), "w", encoding="utf-8") as file:
            for l in file_lines:
                file.write(l)

def move_csvs_to_archive(which_data):
    """if csvs are in present directory, moves them to an archive dir"""
    source_dir = Path()
    archive_dir = Path("./archive")

    archive_dir.mkdir(parents=True, exist_ok=True)

    for file_path in source_dir.iterdir():
        if str(file_path).endswith(".csv") and which_data in str(file_path):
            shutil.move(str(file_path), str(archive_dir) + "/" + str(file_path))


def get_filename(which_data):
    """
    creates filename for csvs for both bills and news
    which_data should be either 'bill' or 'news'
    """
    now = datetime.now().strftime("%m-%d-%y|%H:%M")
    filename = f"{which_data}|{now}.csv"
    return filename
