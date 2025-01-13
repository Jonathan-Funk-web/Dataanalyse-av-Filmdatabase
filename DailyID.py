import os
import sys
import gzip
import shutil
from pathlib import Path
from urllib.request import urlretrieve
from datetime import datetime, timedelta
import requests
import json
import time

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

def download_daily_ID(info: str="movie", filename: str="ID_list") -> None:
    """
    Downloads the file form the url given.
    Args:
        info (str): The info to find, Available parapmetres: `movie`,`tv_series`,`person`,`collection`,`keyword` and `production_company` 
        filename (str): The name of the file you are downloading.  (without file format)
    """

    print(info)

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

def filter_ID_list(import_location: str = Path("Data/movie_id_list.json")) -> list:
    """
    Filters the ID list for just the ID. Also filters out media tagged as either `adult` or `video` WARNING: Replaces old file.
    Args:
        import_location (str): The ID list that will be filtered.
    Returns:
        list: list of just the ID and the amount of `adult` and `video` removed.
    """
    #TODO: add the `video` and `adult` list to variables so this is more generalized.
    with open(import_location, "r", encoding="utf-8") as handle:
        json_data = [json.loads(line) for line in handle]

    original_flie_size = os.path.getsize(import_location)
    id_list = []
    temp_dict = {}
    adult_counter = 0 #Increments each time a media is tagged "Adult" (this should be 0 due to the list im downloading, but just implementing it for fun)
    video_counter = 0 #Increments each time a media is tagged "Video"

    for i in range(len(json_data)):
        
        if json_data[i].get("adult"):
            adult_counter = adult_counter + 1
            continue

        if json_data[i].get("video"):
            video_counter = video_counter + 1
            continue

        progressBar(i,len(json_data))
        id_list.append(json_data[i]["id"])
        

    temp_dict.update({"id_list":id_list})
    temp_dict.update({"video_counter":video_counter})
    temp_dict.update({"adult_counter":adult_counter})

    with open(import_location, "w", encoding="utf-8") as file:
        file.write(json.dumps(temp_dict))

    
    print("Old file size: %s bytes\nNew file size: %s bytes\nFilesize is %s bytes smaller i.e. %s%% smaller." % (original_flie_size,os.path.getsize(import_location),(original_flie_size-os.path.getsize(import_location)),(100*(original_flie_size-os.path.getsize(import_location)))/original_flie_size))

def progressBar(count_value, total, suffix=''):
    bar_length = 100
    filled_up_Length = int(round(bar_length* count_value / float(total)))
    percentage = round(100.0 * count_value/float(total),1)
    bar = '=' * filled_up_Length + '-' * (bar_length - filled_up_Length)
    sys.stdout.write('[%s] %s%s ...%s\r' %(bar, percentage, '%', suffix))
    sys.stdout.flush()
    #This code is Contributed by PL VISHNUPPRIYAN from url: https://www.geeksforgeeks.org/progress-bars-in-python/


# def check_for_new_IDs() -> bool:
#     with open(Path(r"Data\todays_list_movies.json"), "r") as file:
#         json_data = json.load(file)
#     previous_full_id_list = json_data["id_list"]
#     return

# check_for_new_IDs()