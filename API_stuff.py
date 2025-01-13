import json, os, logging, requests
from pathlib import Path
from dotenv import load_dotenv
from DailyID import progressBar

url_auth = "https://api.themoviedb.org/3/authentication"
url_get_movies = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&sort_by=popularity.desc"
url_get_movie_genres = "https://api.themoviedb.org/3/genre/movie/list?language=en"
url_get_people_list = "https://api.themoviedb.org/3/person/changes?page=1"
url_get_movie_details = "https://api.themoviedb.org/3/movie/"

def get_data(url: str) -> str:
    """
    Gets data from TMDB's API.
    
    Args:
        url (str): The URL to use with the API.
        export_location (str): The file location for .json.
        write (bool): If True, prints the data gathered to the file.
    
    Returns:
        str:  Data gathered.
    """

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
    
    #Error handling
    if not response_text.get("success", True):
        logging.critical("API connection failed, error: %s\n%s" % (response_text["status_code"],response_text["status_message"]))
        return
    

    return response_text

def get_movie_info(id:int) -> dict:
    """
    Gets the general movie info from the given movie id.
    args:
        id (int): TMDB id for the movie.
    returns:
        dict: Data gathered.
    """
    return get_data(url = "https://api.themoviedb.org/3/movie/"+str(id))

def get_movie_credits(id:int) -> dict:
    """
    Gets the credits for movie the given movie id.
    args:
        id (int): TMDB id for the movie.
    returns:
        dict: Data gathered.
    """
    return get_data(url = "https://api.themoviedb.org/3/movie/"+ str(id) + "/credits?language=en-US")

def get_directors(id_list_location:str = r"Data\people_ID_list.json"):
    with open(Path(id_list_location), "r") as file:
        json_data = json.load(file)
    
    progress = 0
    
    # for person_id in json_data["id_list"]:
    #     progressBar(progress, len(json_data["id_list"]))

    #     person_info = get_data("https://api.themoviedb.org/3/person/" + str(person_id)[0])
    #     print(type(person_info))
        
    #     progress = progress + 1


    person_info = get_data("https://api.themoviedb.org/3/person/" + str(93364))
    print(person_info)
    
    
    # "Directing"

get_directors()