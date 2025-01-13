import json, os, logging, requests
from pathlib import Path
from dotenv import load_dotenv


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
        str:  Response.
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
    

    return response_text, response

def get_movie_info(id:int) -> dict:
    """
    Gets the general movie info from the given movie id.
    args:
        id (int): TMDB id for the movie.
    returns:
        dict: Data gathered.
    """
    return get_data(url = "https://api.themoviedb.org/3/movie/"+str(id))[0]

def get_movie_credits(id:int) -> dict:
    """
    Gets the credits for movie the given movie id.
    args:
        id (int): TMDB id for the movie.
    returns:
        dict: Data gathered.
    """
    return get_data(url = "https://api.themoviedb.org/3/movie/"+ str(id) + "/credits?language=en-US")[0]
print(get_movie_credits(2))