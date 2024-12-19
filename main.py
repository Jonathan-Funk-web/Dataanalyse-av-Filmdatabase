import os,os.path,requests,json,sys,logging
from pathlib import Path
from dotenv import load_dotenv 

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
    if os.path.exists(Path(export_location)):
        logging.warning(str(Path("Data")) + " already exists")


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

def filter_basic_data(import_location: str, filter: list=["id"]) -> str:
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
    for item in data["results"]:#Adds the media to a dict
        filtered_dict = {}  
        for info in filter:
            if str(info) in item:  
                filtered_dict[info] = item[str(info)]
        if filtered_dict:
            filtered_data.append(filtered_dict)
    filtered_dict = {d['id']: d for d in filtered_data}

    export_location = os.path.join(os.path.dirname(import_location),"Filtered_"+os.path.basename(import_location)) #Adds `Filtered_` to the export file

    with open(export_location, "w") as f:
        json.dump(filtered_dict, f, indent=4)
    f.close()


    return export_location

def get_extra_media_data(import_location: str,export_location: str = "Data/detailed_media.json") -> None:
    """
    Uses TMDB's API to get all info about given media.
.
    Arg:
        import_location (str): The location for the .json file to gather data from.
    """
    with open(import_location, "r") as file:
        data = json.load(file)

    for item in data:
        print(item)
        Details = get_data(url_get_movie_details+item+"?append_to_response=credits%2Ckeywords&language=en-US",write=False)        
        data[item].update({"Details": Details})
    with open(Path(export_location), "w") as file:
        json.dump(data, file, indent=4)
    file.close()
    return

def filter_non_basic_data(import_location:str) -> None:
    ...

def startup():
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


#TODO make it so that these functions does not have to open then close the file every time. Also make the media_id be able to be a int not just str.
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

    weighted_rating = round(weighted_factor*this_media_vote_average + (1-weighted_factor)*all_media_average_vote,2)
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

def get_images(import_location:str, media_id:str, image_type:str="poster", image_size:str="original", collection_image:bool=False) -> str:
    """
    Gets the images for the media.
    
    Args:
        import_location (str): Location for the .json file with the movie data.
        media_id (str): The media you want the income for.
        image_type (str): The image from the media to get. (Supported types: `backdrop` and `poster`)
        image_size (str): The size of the image. (Supported sizes:\n Backdrop: `w300`, `w780`, `w1280`, `original`.\n Poster: `w92`, `w154`, `w185`, `w342`, `w500`, `w780`, `original`.)
        collection_image (bool): If true it gets the images from the collection the media belongs to.
    Returns:
        str: Image URL
    """
    with open(import_location, "r") as file:
        data = json.load(file)
    image_type = image_type + "_path"
    if collection_image:
        if data[media_id]["Details"]["belongs_to_collection"] == None:
            return None
        return "https://image.tmdb.org/t/p/" + image_size + data[media_id]["Details"]["belongs_to_collection"][image_type]
    else:
        return "https://image.tmdb.org/t/p/" + image_size + data[media_id]["Details"][image_type]

def get_countries(import_location:str, media_id:str) -> str:
    """
    Gets the country the media originates from.
    
    Args:
        import_location (str): Location for the .json file with the movie data.
        media_id (str): The media you want the income for.
    Returns:
        str: The country the media originates from.
    """
    with open(import_location, "r") as file:
        data = json.load(file)

    return data[media_id]["Details"]["origin_country"][0]

def get_languages(import_location:str, media_id:str, info_wanted:str="original_language") -> str|list[str]:
    """
    Gets the languages used in the media.
    
    Args:
        import_location (str): Location for the .json file with the movie data.
        media_id (str): The media you want the income for.
        info_wanted (str): The information wanted. (Supported parameters: `original_language` gives the original language for the media. `spoken_languages` gives list of languages spoken in the media.
    Returns:
        str: Language in format `iso_639_1`.
        list[str]: Language in format `iso_639_1`.
    """
    with open(import_location, "r") as file:
        data = json.load(file)
    if info_wanted == "original_language":
        return data[media_id]["Details"]["original_language"]
    if info_wanted == "spoken_languages":
        language_list = []
        for i in range(len(data[media_id]["Details"]["spoken_languages"])):
            language_list.append(data[media_id]["Details"]["spoken_languages"][i]["iso_639_1"])
        return language_list

def get_popularity(import_location:str, media_id:str) -> float:
    """
    Gets the popularity rating for the media.
    
    Args:
        import_location (str): Location for the .json file with the movie data.
        media_id (str): The media you want the income for.
    
    Returns:
        float: Popularity rating
    """
    with open(import_location, "r") as file:
        data = json.load(file)

    return data[media_id]["Details"]["popularity"]

def get_production(import_location:str, media_id:str, info_wanted:str="name", company_nr:int|None=None) -> str|list[str]|int:
    """
    Gets information about the production companies that produced the media.
    
    Args:
        import_location (str): Location for the .json file with the movie data.
        media_id (str): The media you want the income for.
        info_wanted (str): The information wanted. (Supported parameters: \n `logo` gives the url for the logo.\n `name` gives the companies name.\n `country` gives the origin country for the company.\n `amount` gives the amount of production companies involved with the media. \n `name_list` gives the list of names for all the companies involved with the media. \n `country_list` gives the list of all the different origin countries for the companies.)
        company_nr (int): Gives the information for company number `company_nr`. Is not needed for `amount`, `name_list`, `all_countries`.
    Returns:
        str: Information wanted (if used `info_wanted=logo` or `info_wanted=name` )
        list[str]: Information wanted (if used `info_wanted=name_list` or `info_wanted=country_list`, country information is given in format `iso_3166_1`)
        int: Amount of companies (if used `info_wanted=amount`)
    """
    with open(import_location, "r") as file:
        data = json.load(file)


    if info_wanted == "logo":
        if data[media_id]["Details"]["production_companies"][company_nr]["logo_path"] == None:
            print("No url for logo found for company " + data[media_id]["Details"]["production_companies"][company_nr]["name"])
            return
        return "https://image.tmdb.org/t/p/original" + data[media_id]["Details"]["production_companies"][company_nr]["logo_path"]
    if info_wanted == "name":
        return data[media_id]["Details"]["production_companies"][company_nr]["name"]
    if info_wanted == "country":
        return data[media_id]["Details"]["production_companies"][company_nr]["origin_country"]
    if info_wanted == "amount":
        return len(data[media_id]["Details"]["production_companies"])
    if info_wanted == "name_list":
        name_list = []
        for i in range(len(data[media_id]["Details"]["production_companies"])):
            name_list.append(data[media_id]["Details"]["production_companies"][i]["name"])
        return name_list
    if info_wanted == "country_list":
        country_list = []
        for i in range(len(data[media_id]["Details"]["production_companies"])):
            if data[media_id]["Details"]["production_companies"][i]["origin_country"] not in country_list:
                country_list.append(data[media_id]["Details"]["production_companies"][i]["origin_country"])
        return country_list

def get_release_date(import_location:str, media_id:str) -> str:
    """
    Gets the release date for the media (in YYYY-MM-DD).
    
    Args:
        import_location (str): Location for the .json file with the movie data.
        media_id (str): The media you want the income for.
    
    Returns:
        str: Release Date
    """
    with open(import_location, "r") as file:
        data = json.load(file)

    return data[media_id]["Details"]["release_date"]

def get_runtime(import_location:str, media_id:str) -> int:
    """
    Gets the runtime for the media.
    
    Args:
        import_location (str): Location for the .json file with the movie data.
        media_id (str): The media you want the income for.
    
    Returns:
        int: Runtime
    """
    with open(import_location, "r") as file:
        data = json.load(file)

    return data[media_id]["Details"]["runtime"]

    #This is not meatn to be a function, just a template to quickly make new "get_..." functions

def get_cast(import_location:str, media_id:str, info_wanted:list[str]=["name","gender","known_for_department","profile_path","popularity","id"]) -> list[dict]:
    """
    Gets the casting credits for the media.
    
    Args:
        import_location (str): Location for the .json file with the movie data.
        media_id (str): The media you want the income for.
        info_wanted (str): The information wanted. (Supported parameters: `name` gives the actor's name, `gender` gets the actor's gender (`0` = not set / not specified. `1` = female. `2` = male. `3` = non-binary.), `known_for_department` gives the usual department the person works with, `popularity` gives the actor's pupularity score, `profile_path` gives the URL for their image, `id` TMDB id.)
    Returns:
        list[dict]: List of dictionaries, each index in the list is an actor, each dictionary is a K:V pair for their info 
    """

    with open(import_location, "r") as file:
        data = json.load(file)
        actor = {}
        actor_list = []
        for i in range(len(data[media_id]["Details"]["credits"]["cast"])):
            for info in info_wanted:
                actor.update({info:data[media_id]["Details"]["credits"]["cast"][i][info]})
            actor_list.append(actor)
            actor = {}
        return actor_list


    #This is not meatn to be a function, just a template to quickly make new "get_..." functions

def get_crew(import_location:str, media_id:str, info_wanted:list[str]=["name","gender","job","department","known_for_department","profile_path","popularity","id"]) -> list[dict]:
    """
    Gets the crew credits for the media.
    
    Args:
        import_location (str): Location for the .json file with the movie data.
        media_id (str): The media you want the income for.
        info_wanted (str): The information wanted. (Supported parameters: `name` gives the person's name, `gender` gets the person's gender (`0` = not set / not specified. `1` = female. `2` = male. `3` = non-binary.),`job` gives the job the person did on the media `department` gives the department the person worked with, `known_for_department` gives the usual department the person works with, `popularity` gives the person's pupularity score, `profile_path` gives a URL for an image of them, `id` TMDB id.)
    Returns:
        list[dict]: List of dictionaries, each index in the list is a person, each dictionary is a K:V pair for their info 
    """

    with open(import_location, "r") as file:
        data = json.load(file)
        crew = {}
        crew_list = []
        for i in range(len(data[media_id]["Details"]["credits"]["crew"])):
            for info in info_wanted:
                crew.update({info:data[media_id]["Details"]["credits"]["crew"][i][info]})
            crew_list.append(crew)
            crew = {}
        return crew_list


    #This is not meatn to be a function, just a template to quickly make new "get_..." functions

def get_keywords(import_location:str, media_id:str) -> list[str]:
    """
    Gets the keywords for the media.
    
    Args:
        import_location (str): Location for the .json file with the movie data.
        media_id (str): The media you want the income for.

    Returns:
        list[str]: List of the keywords.
    """
    with open(import_location, "r") as file:
        data = json.load(file)
    keywords = []
    for i in range(len(data[media_id]["Details"]["keywords"]["keywords"])):
        keywords.append(data[media_id]["Details"]["keywords"]["keywords"][i]["name"])
    return keywords

    #This is not meatn to be a function, just a template to quickly make new "get_..." functions


get_extra_media_data(Path("Data\Filtered_data.json"))