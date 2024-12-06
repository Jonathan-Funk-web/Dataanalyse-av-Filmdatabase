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

data_wanted = ["title","budget","genres","id","origin_country","original_language","original_title","popularity","production_companies","release_date","revenue","runtime","vote_average","vote_count"]
last_date_checked = 0

#API request 
url_auth = "https://api.themoviedb.org/3/authentication"
url_get_movies = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
url_get_movie_genres = "https://api.themoviedb.org/3/genre/movie/list?language=en"
url_get_newest_movies = "https://api.themoviedb.org/3/movie/changes?page=1"
url_get_people_list = "https://api.themoviedb.org/3/person/changes?page=1"
url_get_movie_details = "https://api.themoviedb.org/3/movie/"
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


#get_data(url_get_movie_details+"912649","Test")
filter_data("Data/Test.json",data_wanted)