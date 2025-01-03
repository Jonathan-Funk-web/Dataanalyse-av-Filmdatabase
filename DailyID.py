import os
import sys
import gzip
import shutil
from pathlib import Path
from urllib.request import urlretrieve
from datetime import datetime, timedelta
import requests


def get_daily_ID_url(info: str) -> str:
    """
    Downloads the newest Daily ID export list, if the time is before 8 am UTC it gets yesterdays url instead.

    Args:
        info (str): The info to find, Available parapmetres: `movie`,`tv_series`,`person`,`collection`,`keyword` and `production_company` 
    returns:
        str: url for downloading daily ID
        str: todays date in MMDDYYYY
    """
    
    valid_info_types = {"movie", "tv_series", "person", "collection", "keyword", "production_company"}

    if info not in valid_info_types:
        sys.exit(f'Invalid parameter for "info". Must be one of: {", ".join(valid_info_types)}')

    today = str(datetime.now().strftime("%m_%d_%Y"))
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%m_%d_%Y")

    #Checks if today is earlier than 8:00 AM UTC (if it is check yesterdays log)
    if int(datetime.now().strftime("%H")) > 8:
        print("Getting Todays daily id's")
        url = "http://files.tmdb.org/p/exports/" + str(info) + "_ids_" + today + ".json.gz"

    else:
        print("Getting Yesyerdays daily id's")
        url = "http://files.tmdb.org/p/exports/" + str(info) + "_ids_" + yesterday + ".json.gz"

    return url

def download_daily_ID(url: str, filename: str) -> None:
    """
    Downloads the file form the url given.
    Args:
        url (str): Get this from `get_daily_ID_url`.
        filename (str): The name of the file you are downloading.  (without file format)
    """


    response = requests.get(url)

    if not response.ok:
        print("request failed")
        return

    start_path = Path("Data") / filename

    with open(str(start_path) + ".gz", mode="wb") as file:
        file.write(response.content)

    #This unzips the .gz file.
    with gzip.open(str(start_path) + ".gz", "rb") as f_in:
        with open(str(start_path) + ".json", "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    os.remove(str(start_path) + ".gz")



    return

