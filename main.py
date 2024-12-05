import os,os.path,requests,json,sys
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
- API URL appending
- Fix the filter_data()
- Remove get_movie_genre() It got decrepit as I learned of this API https://developer.themoviedb.org/reference/movie-details 
- make the get_genre_scoere() actually self made
"""

_data_wanted = ["budget","genres","id","origin_country","original_language","original_title","popularity","production_companies","release_date","revenue","runtime","vote_average","vote_count"]
data_wanted = ["id","title","test"]
last_date_checked = 0

#API request 
url_auth = "https://api.themoviedb.org/3/authentication"
url_get_movies = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
url_get_movie_genres = "https://api.themoviedb.org/3/genre/movie/list?language=en"
url_get_newest_movies = "https://api.themoviedb.org/3/movie/changes?page=1"
url_get_people_list = "https://api.themoviedb.org/3/person/changes?page=1"

#TODO: Work on going through the pages for the api search. Use a loop and change the url with it
def get_data(url: str,location: str) -> None:
    """
    :param url: What API URL to use
    :param Get_new_data: If True, replaces data.json with the new data.
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
    
    with open("Data/" + location + ".json", "w") as f:
        f.write(response_text_formatted)


def filter_data(location: str,filter: list):
    """
    :param data: The data that gets filtered
    :param filter: Whitelist filter on the data file
    :return: Filtered data 
    """
    filtered_data = {}
    with open(location, "r") as file:
        data = json.load(file)

    #TODO: The following code just replaces the dict with the newest value-key pair, find a way to make each movie have its own data
    for info in filter:
        for item in data["results"]:
            filtered_data.update({"Movie nr.":i}) 
            if str(info) in item:
                print(filtered_data)
                filtered_data.update({info:item[str(info)]})


    print(filtered_data)
    return


filter_data("Data/data.json",data_wanted)


def get_movie_genre(genre_id=None):
    """
    Uses the API to get the list of genre-id pairs. Then it writes it to "Data/movie-genres.json", if that file already exists then it does not write it.
    :return: If parameter is empty, returns a list of all genre ids. if parameter is not empty, returns the name of the genre_id
    """

    if not os.path.isfile("Data/movie-genres.json"): #Does an API call if the .json file is missing
        print("Data/movie-genres.json does not exist. \nMaking new movie-genres.json file.")
        get_data(url_get_movie_genres,"movie-genres")
    
    f = open("Data/movie-genres.json","r")
    data = json.load(f)
    
    if genre_id is None: #Prints the list of genres
        genre_id_list_keys = []
        genre_id_list_values = []
        genre_id_list_dict = {}
        for i in data["genres"]:
            genre_id_list_keys.append(i["id"])
            genre_id_list_values.append(i["name"])
        for key in genre_id_list_keys:
            for value in genre_id_list_values:
                genre_id_list_dict[key] = value
                genre_id_list_values.remove(value)
                break
        return genre_id_list_dict


    if genre_id is not None:
        for i in data["genres"]:
            if i["id"] == genre_id:
                return i["name"]
        print("Did not find a genre with id: " + str(genre_id))
    f.close()

def genre_vote_score(data: str): #TODO: Make it so that this function outputs both genre_averages and genre_counts in to on dict. Also have it take in to account vote_count.
    """
    Finds the rating for each genre. It takes each movies "vote_avrage" and adds it to each genres total sum (so if a movie has 2 genres each genre gets the movies "vote_avrage")
    """
    genre_ratings = {}
    genre_counts = {}

    with open("Data/filtered_data.json", 'r') as file:
        movies = json.load(file)

    for movie in movies:
        rating = movie['vote_average']
        for genre_id in movie['genre_ids']:
            genre_name = get_movie_genre().get(genre_id)
            if genre_name:
                if genre_name not in genre_ratings:
                    genre_ratings[genre_name] = 0
                    genre_counts[genre_name] = 0
                genre_ratings[genre_name] += rating
                genre_counts[genre_name] += 1

    genre_averages = {}
    for genre_name in genre_ratings:
        average_rating = genre_ratings[genre_name] / genre_counts[genre_name]
        genre_averages[genre_name] = average_rating

    return genre_averages,genre_counts


