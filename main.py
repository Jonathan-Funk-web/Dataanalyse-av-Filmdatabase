import os,requests,json,sys
from dotenv import load_dotenv 


Get_new_data = True #If true, does a API request, if false uses data in data.json
media_list = [] 
adult_list = []
genre_list = {}
data_wanted = ["genre_ids","id","original_language","title","vote_average","vote_count"]

#API request 
url_auth = "https://api.themoviedb.org/3/authentication"
url_get_movies = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
url_get_movie_genres = "https://api.themoviedb.org/3/genre/movie/list?language=en"


#TODO: Work on going through the pages for the api search. Use a loop and change the url with it

def get_data(url,Get_new_data: bool = True, Filter_data: bool = True):
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
        print(response_text_formatted)
        if not response_text.get("success", True):
            sys.exit("API conection failed, error: %s\n%s" % (response_text["status_code"],response_text["status_message"]))
        
        #TODO: Make the open function dependant on what URL we use, so that we get a new file if i get the genres for example.
        with open("data.json", "w") as f:
            f.write(response_text_formatted)
    else:
        print("Did not get new data, used old data. \n")
        with open("data.json") as f:
            response_text = json.load(f)

    if url != url_auth:   
        if url == url_get_movies:    
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

get_data(url_get_movies)

