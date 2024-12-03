import os,os.path,requests,json,sys
from dotenv import load_dotenv 


Get_new_data = True #If true, does a API request, if false uses data in data.json
media_list = [] 
adult_list = []
genre_list = {}
data_wanted = ["genre_ids","id","original_language","title","vote_average","vote_count"]
last_date_checked = 0

#API request 
url_auth = "https://api.themoviedb.org/3/authentication"
url_get_movies = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
url_get_movie_genres = "https://api.themoviedb.org/3/genre/movie/list?language=en"
url_get_newest_movies = "https://api.themoviedb.org/3/movie/changes?page=1"
url_get_people_list = "https://api.themoviedb.org/3/person/changes?page=1"


#TODO: Work on going through the pages for the api search. Use a loop and change the url with it

def get_data(url,location, Get_new_data: bool = True, Filter_data: bool = True):
    """
    :param url: What API URL to use
    :param Get_new_data: If True, replaces data.json with the new data.
    """
    if Get_new_data:
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
    else:
        print("Did not get new data, used old data. \n")
        with open("Data/" + location + ".json") as f:
            response_text = json.load(f)

    if url != url_auth:   
        if (url == url_get_movies) and (Filter_data == True):    
            data = response_text["results"]
            filter_data(data,data_wanted)


def filter_data(data,filter):
    """
    :param data: The data that gets filtered
    :param filter: Whitelist filter on the data file
    :return: Filtered data
    """
    for i in range(0,len(data)):
        if data[i]["adult"]: #If the API fetch fails the filter somehow, it appends the adult movies here
            print("is adult")
            adult_list.append(data[i]["title"])
            continue

        temp_dictionary = {} #Adds the JSON data as dictionaries, think of it as making the json smaller
        for j in filter:
            temp_dictionary.update({j:data[i][j]})
        media_list.append(temp_dictionary)

    with open("filtered_data.json", "w") as outfile: 
        json.dump(media_list, outfile, indent=4)


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
        #print("Genres found: ")
        genre_id_list_keys = []
        genre_id_list_values = []
        genre_id_list_dict = {}
        for i in data["genres"]:
            #print(" -" + i["name"] + " has id: " + str(i["id"]))
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






print(genre_vote_score("Data/filtered_data.json"))
