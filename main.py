import os,os.path,requests,json,sys,logging
from pathlib import Path
from dotenv import load_dotenv 
import getmediainfo as gmi

{ #notes
### THE TASK ###
"""
Do data analasys of the following:
- What directors has directed the most movies/tv-shows
- What actors have been the most active
- What genres has been most popular each decade
"""

### THE PLAN ###
"""
1. Get movie/tv-show (hearafter called just "media") with get_data() using a discovery API link
2. Filter the data from step 1. with filter_data(id)
3. Use get_data() with the id's gotten from step 2. to get extended info on the media
4. Use filter_data(data_wanted) to get the data i am going to use for my data analasys
5. Put that up in a graph (via a .ipynb file since codespaces are wack >:[ )
6. Be proud  (Mandatory)
"""

### PROGRESS ###
"""
- I have set up the git to be able to backup/work from different places.
- I have managed to learn: TMDB's API, API, .JSON, .env
- I have made get_data() that gets data from TMDB's API.
- I have made filter_data() that goes through a .JSON file and returns only the data I want (Might make this so generalized that I will use it for other projects woo) 
"""

### TODO ###
"""
- API Pagination
- make the get_genre_scoere()
- make all my code consistent (it is ugly atm :( )
""" }
#Data to whitelest from the .json
data_wanted = ["title","original_title","genres","keywords","origin_country","original_language","spoken_languages","budget","revenue","production_companies","production_countries","credits","release_date","status","runtime","popularity","vote_average","vote_count"]
credits_data_wanted = ["gender","known_for_department","name","popularity"]
last_date_checked = 0 

#Setting up logger:
logging.basicConfig(format="TIME: %(asctime)s | LINE: %(lineno)s | %(levelname)s -> %(message)s")

#API request 
url_auth = "https://api.themoviedb.org/3/authentication"
url_get_movies = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
url_get_movie_genres = "https://api.themoviedb.org/3/genre/movie/list?language=en"
url_get_people_list = "https://api.themoviedb.org/3/person/changes?page=1"
url_get_movie_details = "https://api.themoviedb.org/3/movie/"

#TODO: Work on going through the pages for the api search. Use a loop and change the url with it
def get_data(url: str, export_location: str="Data/data.json", write: bool=True) -> str:
    """
    Gets data from TMDB's API and returns it as a .json file at export_location.
    
    Args:
        url (str): The URL to use with the API.
        export_location (str): The file location for .json.
        write (bool): If True, prints the data gathered to the file.
    
    Returns:
        str: All the data on the .json file.
    """
    logging.debug("Starting get_data(%s)" % url)
    #Chacks if we have the data beforehand.


    #API key security
    load_dotenv() 
    Auth_key = os.getenv("MOVIEDB_APP_AUTH_DOMAIN")

    #Got this from TMDB api documentation
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer %s" % Auth_key
    }
    response = requests.get(url, headers=headers)
    response_text = json.loads(response.text)
    response_text_formatted = json.dumps(response_text, indent=4)
    #Error handling
    if not response_text.get("success", True):
        logging.critical("API connection failed, error: %s\n%s" % (response_text["status_code"],response_text["status_message"]))
        return
    
    if write:
        if not os.path.exists(Path("Data")):
            logging.info("Did not find dir named Data")
            os.makedirs(Path("Data"))
            logging.info("Dir Data made")
        with open(Path(export_location), "w") as f:
            f.write(response_text_formatted)
            logging.debug("Writing data to file: %s" % (Path(export_location)))
        logging.info("returning response text")

    logging.info("get_data(%s) done!" % url)
    return response_text

def filter_basic_data(import_location: str="Data/data.json", filter: list=["id","title"]) -> str:
    """
    Filters the .json data from import_location, if the .json has a object with a name that is on the whitelist filter it is copied over for the next file. If it is not it is ignored.
    When finished, it exports it to the same directory but with the prefix `filtered_` to its name.

    Args:
        import_location (str): The location for the .json file.
        filter (list of str): A list for what to whitelist.
    Returns:
        str: Location for the new .json file.
    """

    try:
        filter[0]
    except:
        logging.warning("Filter cant be empty")

    print("Filtering %s with whitelist-filter %s" % (import_location,filter))
    import_location = Path(import_location) # Maks the directory path complient with the os.
    filtered_data = []
    with open(import_location, "r") as file:
        data = json.load(file)
    print(str(import_location) + " loaded!")
    for item in data["results"]: # Adds the media to a dict
        filtered_dict = {}  
        for info in filter:
            if str(info) in item:  
                filtered_dict[info] = item[str(info)]
        if filtered_dict:
            filtered_data.append(filtered_dict)
    filtered_dict = {d['id']: d for d in filtered_data}

    export_location = os.path.join(os.path.dirname(import_location),"Filtered_"+os.path.basename(import_location)) # Adds `Filtered_` to the export file

    with open(export_location, "w") as f:
        json.dump(filtered_dict, f, indent=4)
    f.close()


    return export_location

def get_extra_media_data(import_location: str,export_location: str = "Data/detailed_media_data.json") -> None:
    """
    Uses TMDB's API to get all info about given media.
.
    Arg:
        import_location (str): The location for the .json file to gather data from.
    """
    with open(import_location, "r") as file:
        data = json.load(file)

    for item in data:
        Details = get_data(url_get_movie_details+item+"?append_to_response=credits%2Ckeywords&language=en-US",write=False)        
        data[item].update(Details)
        print(data[item]["title"])

        
    with open(Path(export_location), "w") as file:
        json.dump(data, file, indent=4)
    return



def filter_non_basic_data(import_location:str) -> None:
    ...

def set_api_key(key:str) -> bool:
    """
    Saves the API key in a .env file. (MAKE SURE TO ADD .env TO YOUR .gitignore FILE IF YOU HAVE NOT DONE SO ALLREADY)
    
    Args:
        key (str): API key.
    Returns:
        bool: Wether the API key works or not.
    """
    logging.info("Setting API key")
    f = open(".env", "w")
    f.write("MOVIEDB_APP_AUTH_DOMAIN=" + key)
    logging.info("API key set")
    logging.debug("Testing if API key works")
    f.close()

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + key
    }

    response = requests.get("https://api.themoviedb.org/3/authentication", headers=headers)

    if json.loads(response.text)["success"]:
        logging.info("API is working")
    else:
        logging.error("Your API key is not valid")
    
    return json.loads(response.text)["success"]

def startup(key:str):
    """
    Gives you the data in a quick and easy way.

    Args: 
        key(str): Your TMDB API key. 
    """
    

    print("Setting up API key.")
    if set_api_key(key):
        print("API key set successfully.")
    else:
        sys.exit("Failed to set API key.")
    get_data(url_get_movies)
    get_extra_media_data(filter_basic_data())
    if os.path.exists(Path(r"Data\data.json")):
        os.remove(Path(r"Data\data.json"))
    if os.path.exists(Path(r"Data\Filtered_data.json")):
        os.remove(Path(r"Data\Filtered_data.json"))
    



# print(type(gmi.get_votes(r"Data\detailed_media_data.json","845781")))