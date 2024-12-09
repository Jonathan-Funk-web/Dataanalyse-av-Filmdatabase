import os,os.path,requests,json,sys
from dotenv import load_dotenv 

### THE TASK ###
"""
MOVIEDB_APP_AUTH_DOMAIN
MOVIEDB_APP_API_KEY
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
- API URL appending
- Fix the filter_data()
- Remove get_movie_genre() It got decrepit as I learned of this API https://developer.themoviedb.org/reference/movie-details 
- make the get_genre_scoere() actually self made
- make all my code consistent (it is ugly atm :( )
"""
#Data to whitelest from the .json
data_wanted = ["budget","genres","keywords","origin_country","original_language","original_title","popularity","production_companies","production_coujntries","release_date","revenue","runtime","spoken_languages","status","title","vote_average","vote_count"]
credits_data_wanted = ["gender","known_for_department","name","popularity"]
last_date_checked = 0


#API request 
url_auth = "https://api.themoviedb.org/3/authentication"
url_get_movies = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
url_get_movie_genres = "https://api.themoviedb.org/3/genre/movie/list?language=en"
url_get_newest_movies = "https://api.themoviedb.org/3/movie/changes?page=1"
url_get_people_list = "https://api.themoviedb.org/3/person/changes?page=1"
url_get_movie_details = "https://api.themoviedb.org/3/movie/"
#TODO: Work on going through the pages for the api search. Use a loop and change the url with it
def get_data(url: str,location: str,write:bool=True) -> None:
    """
    :param url: What API URL to use
    :param Get_new_data: If True, replaces data.json with the new data.
    :return: Returns the data it gathers
    """
    load_dotenv() 
    Auth_key = os.getenv("MOVIEDB_APP_AUTH_DOMAIN")
    #TODO: make this only get data if data.json is empty (as to reduce the amount of searches)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer %s" % Auth_key
    }

    response = requests.get(url, headers=headers)
    response_text = json.loads(response.text)
    response_text_formatted = json.dumps(response_text, indent=4)
    if not response_text.get("success", True):
        sys.exit("API connection failed, error: %s\n%s" % (response_text["status_code"],response_text["status_message"]))
    
    if write:
        with open("Data/" + location + ".json", "w") as f:
            f.write(response_text_formatted)
    
    return response_text


def filter_basic_data(location: str,filter: list):
    """
    :param data: The data that gets filtered
    :param filter: Whitelist filter on the data file
    :return: Filtered data 
    """
    filtered_data = []
    with open(location, "r") as file:
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
    new_location = location[location.find('/') + 1:-5]
    
    with open("Data/filtered_" + new_location + ".json", "w") as f:
        json.dump(filtered_dict, f, indent=4)
    f.close()

def get_extra_media_data(location: str):
    
    with open(location, "r") as file:
        data = json.load(file)

    for item in data:
        Details = get_data(url_get_movie_details+item+"?append_to_response=credits%2Ckeywords&language=en-US","TEST",write=False)        
        data[item].update({"Details": Details})
    with open("Data/extra_media_details.json", "w") as file:
        json.dump(data, file, indent=4)

    return


def filter_detailed_data(data_location: str, filter: list=["title","id","homepage"]):
    with open(data_location, "r") as file:
        data = json.load(file)

    filtered_data = {}
    
    for item in data:
        for filtered in filter:
            filtered_data.update({item:data[item]["Details"][filtered]})

    print(filtered_data)
    return


# filter_basic_data("Data/data.json",["id"]) 
# get_extra_media_data("Data/filtered_data.json")
filter_detailed_data("Data/extra_media_details.json")