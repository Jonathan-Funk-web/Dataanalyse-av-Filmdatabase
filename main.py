import os,os.path,requests,json,sys,math
from dotenv import load_dotenv 

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
"""
#Data to whitelest from the .json
data_wanted = ["title","original_title","genres","keywords","origin_country","original_language","spoken_languages","budget","revenue","production_companies","production_countries","credits","release_date","status","runtime","popularity","vote_average","vote_count"]
credits_data_wanted = ["gender","known_for_department","name","popularity"]
last_date_checked = 0


#API request 
url_auth = "https://api.themoviedb.org/3/authentication"
url_get_movies = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
url_get_movie_genres = "https://api.themoviedb.org/3/genre/movie/list?language=en"
url_get_people_list = "https://api.themoviedb.org/3/person/changes?page=1"
url_get_movie_details = "https://api.themoviedb.org/3/movie/"

#TODO: Work on going through the pages for the api search. Use a loop and change the url with it
def get_data(url: str, export_location: str="newdata.json", write: bool=True) -> str:
    """
    Gets data from TMDB's API and returns it as a .json file at export_location.
    
    Args:
        url (str): The URL to use with the API.
        export_location (str): The file location for .json.
        write (bool): If True, prints the data gathered to the file.
    
    Returns:
        str: All the data on the .json file.
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
    response_text_formatted = json.dumps(response_text, indent=4)
    #Error handling
    if not response_text.get("success", True):
        sys.exit("API connection failed, error: %s\n%s" % (response_text["status_code"],response_text["status_message"]))
    
    if write:
        with open(export_location, "w") as f:
            f.write(response_text_formatted)
    
    return response_text


def filter_basic_data(import_location: str, filter: list) -> str:
    """
    Filters the .json data from import_location, if the .json has a object with a name that is on the whitelist filter it is copied over for the next file. If it is not it is ignored.
    When finished, it exports it to the same directory but with the prefix `filtered_` to its name.

    Args:
        import_location (str): The location for the .json file.
        filter (list of str): A list for what to whitelist.
    Returns:
        str: Location for the new .json file.
    """
    filtered_data = []
    with open(import_location, "r") as file:
        data = json.load(file)

    for item in data["results"]:#Adds the media to a dict
        filtered_dict = {}  
        for info in filter:  
            if str(info) in item:  
                filtered_dict[info] = item[str(info)]
        if filtered_dict:
            filtered_data.append(filtered_dict)
    filtered_dict = {d['id']: d for d in filtered_data}
    #Trimming the location string
    export_location = import_location[import_location.find('/') + 1:-5]
    
    with open("Data/filtered_" + export_location + ".json", "w") as f:
        json.dump(filtered_dict, f, indent=4)
    f.close()

    return "Data/filtered_" + export_location + ".json"


def get_extra_media_data(import_location: str) -> None:
    """
    Uses TMDB's API to get all info about given media.

    Arg:
        import_location (str): The location for the .json file to gather data from.
    """

    with open(import_location, "r") as file:
        data = json.load(file)

    for item in data:
        Details = get_data(url_get_movie_details+item+"?append_to_response=credits%2Ckeywords&language=en-US","TEST",write=False)        
        data[item].update({"Details": Details})

    with open("Data/extra_media_details.json", "w") as file:
        json.dump(data, file, indent=4)
    file.close()

def filter_non_basic_data():
    pass
    #This function will use the functions below to filter the data one final time, and get what i will use for the graphs and such. Soon™

#TODO make it so that these functions does not have to open then close the file every time.
def get_votes(import_location:str, media_id:str, weighted:bool = False) -> float:
    """
    Gets the average votes for the media.

    Args:
        import_location (str): Location for the .json file with the movie data.
        media_id (str): The media to find the votes for.
        weighted (bool): If `True` returns the rating with a weight algorithm.

    Returns:
        float: rating
    """
    #I used this as a guideline https://math.stackexchange.com/questions/41459/how-can-i-calculate-most-popular-more-accurately/41513
    with open(import_location, "r") as file:
        data = json.load(file)

    all_media_highest_vote_amount = 0
    all_media_average_vote = 0
    for media in data:
        all_media_average_vote += data[media]["vote_average"]
        if all_media_highest_vote_amount < data[media]["vote_count"]:
            all_media_highest_vote_amount = data[media]["vote_count"]
    all_media_average_vote = all_media_average_vote/len(data)
    this_media_vote_average = data[media_id]["vote_average"]
    this_media_vote_count = data[media_id]["vote_count"]
    weighted_factor = this_media_vote_count/all_media_highest_vote_amount

    weighted_rating = round(weighted_factor*this_media_vote_average + (1-weighted_factor)*all_movie_average_vote,2)
    file.close()
    if weighted:
        return weighted_rating
    else:
        return this_media_vote_average

def get_income(import_location:str, media_id:str) -> float:
    """
    Finds the income for media
    
    Args:
        import_location (str): Location for the .json file with the movie data.
        media_id (str): The media you want the income for.
    
    Returns:
        float: Total income for a movie (revenue - budget).
    """
    with open(import_location, "r") as file:
        data = json.load(file)
    return data[media_id]["Details"]["revenue"] - data[media_id]["Details"]["budget"]

def get_title(import_location:str, media_id:str, mode:int=0) -> str | bool:
    """
    Gets the title for the media.
    
    Args:
        import_location (str): Location for the .json file with the movie data.
        media_id (str): The media you want the income for.
        mode (int): 0 gives `title`. 1 gives `original_title`. 2 gives a bool for if `title == original_title` 
    Returns:
        str: Title for the media.
    """
    with open(import_location, "r") as file:
        data = json.load(file)
    
    #assert mode not in [0,1,2], "Mode (third argument) was %s\nIt has to be either: 0 or 1 or 2" % mode
    if mode == 0:
        return data[media_id]["Details"]["title"]
    elif mode == 1:
        return data[media_id]["Details"]["original_title"]
    elif mode == 2:
        return data[media_id]["Details"]["title"] == data[media_id]["Details"]["original_title"]

    #TODO figure out if i should place file.close() here or not

def get_popularity(import_location:str, media_id:str) -> float:
    """
    Gets the popularity rating in the media.
    
    Args:
        import_location (str): Location for the .json file with the movie data.
        media_id (str): The media you want the income for. 
    
    Returns:
        float: Popularity Rating
    """
    with open(import_location, "r") as file:
        data = json.load(file)

    return data[media_id]["Details"]["popularity"]

def get_genres(import_location:str, media_id:str) -> list:
    """
    Gets the genres for the media.
    
    Args:
        import_location (str): Location for the .json file with the movie data.
        media_id (str): The media you want the income for.
    
    Returns:
        list: Name of the genres. 
    """
    with open(import_location, "r") as file:
        data = json.load(file)
    
    genres = []
    for i in data[media_id]["Details"]["genres"]:
        genres.append(i["name"])
    return genres


def get_PLACEHOLDER(import_location:str, media_id:str) -> None:
    """
    Gets the ...  in the media.
    
    Args:
        import_location (str): Location for the .json file with the movie data.
        media_id (str): The media you want the income for.
    
    Returns:
        ...
    """
    with open(import_location, "r") as file:
        data = json.load(file)

    return data[media_id]["Details"]["PLACEHOLDER"]

    #This is not meatn to be a function, just a template to quickly make new "get_..." functions

print(get_genres("Data/extra_media_details.json","912649"))