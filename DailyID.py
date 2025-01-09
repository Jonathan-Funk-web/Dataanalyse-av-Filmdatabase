import os
import sys
import gzip
import shutil
from pathlib import Path
from urllib.request import urlretrieve
from datetime import datetime, timedelta
import requests


def get_daily_ID_url(info: str,use_yesterday: bool = False) -> str:
    """
    Downloads the newest Daily ID export list, if the time is before 8 am UTC it gets yesterdays url instead.

    Args:
        info (str): The info to find, Available parapmetres: `movie`,`tv_series`,`person`,`collection`,`keyword` and `production_company` 
        use_yesterday (bool): If True: tries to download using yesterdays list.
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
    if (int(datetime.now().strftime("%H")) > 8) and not use_yesterday:
        print("Getting Todays daily id's")
        url = "http://files.tmdb.org/p/exports/" + str(info) + "_ids_" + today + ".json.gz"

    else:
        print("Getting Yesyerdays daily id's")
        url = "http://files.tmdb.org/p/exports/" + str(info) + "_ids_" + yesterday + ".json.gz"

    #TODO: Add a way for it to go back one day at a time untuil it finds a valid URL (i.e. add redundency) 
    return url

def download_daily_ID(info: str, filename: str) -> None:
    """
    Downloads the file form the url given.
    Args:
        info (str): The info to find, Available parapmetres: `movie`,`tv_series`,`person`,`collection`,`keyword` and `production_company` 
        filename (str): The name of the file you are downloading.  (without file format)
    """

    url = get_daily_ID_url(info)

    response = requests.get(url)

    if not response.ok:
        print("request failed")
        url = get_daily_ID_url(info,use_yesterday=True)
        response = requests.get(url)

    if not os.path.isdir(Path("Data")):
        print("%s does not exist, making it now" % Path("Data"))
        os.makedirs(Path("Data"))

    start_path = Path("Data") / filename

    with open(str(start_path) + ".gz", mode="wb") as file:
        file.write(response.content)

    #This unzips the .gz file.
    with gzip.open(str(start_path) + ".gz", "rb") as f_in:
        with open(str(start_path) + ".json", "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    os.remove(str(start_path) + ".gz")



    return

