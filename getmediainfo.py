import json
from pathlib import Path


def load_json(import_location:str)->dict:
    """
    Used by the other functions in this module to open the `import_location`
    Args:
        import_location (str): Location of the datafile to use.
    Returns:
        dict: .json file.
    """
    with open(Path(import_location), "r") as file:
        return json.load(file)

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
    data = load_json(import_location)

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

    weighted_rating = weighted_factor*this_media_vote_average + (1-weighted_factor)*all_media_average_vote
    if weighted:
        return round(weighted_rating,2)
    else:
        return round(this_media_vote_average,2)

def get_budget(import_location:str, media_id:str) -> float:
    """
    Finds the budget for media
    
    Args:
        import_location (str): Location for the .json file with the movie data.
        media_id (str): The media you want the budget for.
    
    Returns:
        float: Total budget for a movie.
    """
    data = load_json(import_location)

    return data[media_id]["budget"]

def get_revenue(import_location:str, media_id:str) -> float:
    """
    Finds the revenue for media
    
    Args:
        import_location (str): Location for the .json file with the movie data.
        media_id (str): The media you want the revenue for.
    
    Returns:
        float: Revenue for a movie.
    """
    data = load_json(import_location)

    return data[media_id]["revenue"]

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
    data = load_json(import_location)

    
    #assert mode not in [0,1,2], "Mode (third argument) was %s\nIt has to be either: 0 or 1 or 2" % mode
    if mode == 0:
        return data[media_id]["title"]
    elif mode == 1:
        return data[media_id]["original_title"]
    elif mode == 2:
        return data[media_id]["title"] == data[media_id]["original_title"]

def get_popularity(import_location:str, media_id:str) -> float:
    """
    Gets the popularity rating in the media.
    
    Args:
        import_location (str): Location for the .json file with the movie data.
        media_id (str): The media you want the income for. 
    
    Returns:
        float: Popularity Rating
    """
    data = load_json(import_location)


    return data[media_id]["popularity"]

def get_genres(import_location:str, media_id:str) -> list:
    """
    Gets the genres for the media.
    
    Args:
        import_location (str): Location for the .json file with the movie data.
        media_id (str): The media you want the income for.
    
    Returns:
        list: Name of the genres. 
    """
    data = load_json(import_location)

    
    genres = []
    for i in data[media_id]["genres"]:
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
    data = load_json(import_location)

    image_type = image_type + "_path"
    if collection_image:
        if data[media_id]["belongs_to_collection"] == None:
            return None
        return "https://image.tmdb.org/t/p/" + image_size + data[media_id]["belongs_to_collection"][image_type]
    else:
        return "https://image.tmdb.org/t/p/" + image_size + data[media_id][image_type]

def get_countries(import_location:str, media_id:str) -> str:
    """
    Gets the country the media originates from.
    
    Args:
        import_location (str): Location for the .json file with the movie data.
        media_id (str): The media you want the income for.
    Returns:
        str: The country the media originates from.
    """
    data = load_json(import_location)


    return data[media_id]["origin_country"][0]

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
    data = load_json(import_location)

    if info_wanted == "original_language":
        return data[media_id]["original_language"]
    if info_wanted == "spoken_languages":
        language_list = []
        for i in range(len(data[media_id]["spoken_languages"])):
            language_list.append(data[media_id]["spoken_languages"][i]["iso_639_1"])
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
    data = load_json(import_location)


    return data[media_id]["popularity"]

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
    data = load_json(import_location)



    if info_wanted == "logo":
        if data[media_id]["production_companies"][company_nr]["logo_path"] == None:
            print("No url for logo found for company " + data[media_id]["production_companies"][company_nr]["name"])
            return
        return "https://image.tmdb.org/t/p/original" + data[media_id]["production_companies"][company_nr]["logo_path"]
    if info_wanted == "name":
        return data[media_id]["production_companies"][company_nr]["name"]
    if info_wanted == "country":
        return data[media_id]["production_companies"][company_nr]["origin_country"]
    if info_wanted == "amount":
        return len(data[media_id]["production_companies"])
    if info_wanted == "name_list":
        name_list = []
        for i in range(len(data[media_id]["production_companies"])):
            name_list.append(data[media_id]["production_companies"][i]["name"])
        return name_list
    if info_wanted == "country_list":
        country_list = []
        for i in range(len(data[media_id]["production_companies"])):
            if data[media_id]["production_companies"][i]["origin_country"] not in country_list:
                country_list.append(data[media_id]["production_companies"][i]["origin_country"])
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
    data = load_json(import_location)


    return data[media_id]["release_date"]

def get_runtime(import_location:str, media_id:str) -> int:
    """
    Gets the runtime for the media.
    
    Args:
        import_location (str): Location for the .json file with the movie data.
        media_id (str): The media you want the income for.
    
    Returns:
        int: Runtime
    """
    data = load_json(import_location)


    return data[media_id]["runtime"]

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

    data = load_json(import_location)
    image_url = "https://image.tmdb.org/t/p/original"
    actor = {}
    actor_list = []
    for i in range(len(data[media_id]["credits"]["cast"])):
        for info in info_wanted:
            if info == "profile_path":
                profile_path = data[media_id]["credits"]["cast"][i].get(info, "")
                if profile_path:
                    actor.update({info: f"{image_url}{profile_path}"})
                else:
                    actor.update({info: None})  # In case profile_path is missing
            else:
                actor.update({info:data[media_id]["credits"]["cast"][i][info]})
        actor_list.append(actor)
        actor = {}
    return actor_list

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

    data = load_json(import_location)
    base_url = "https://image.tmdb.org/t/p/original"
    crew = {}
    crew_list = []
    for i in range(len(data[media_id]["credits"]["crew"])):
        for info in info_wanted:
            if info == "profile_path":
                # If profile_path exists, construct the full URL
                profile_path = data[media_id]["credits"]["crew"][i].get(info, "")
                if profile_path:
                    crew.update({info: f"{base_url}{profile_path}"})
                else:
                    crew.update({info: None})  # In case profile_path is missing
            else:
                crew.update({info: data[media_id]["credits"]["crew"][i].get(info)})
        crew_list.append(crew)
        crew = {}
    return crew_list

def get_keywords(import_location:str, media_id:str) -> list[str]:
    """
    Gets the keywords for the media.
    
    Args:
        import_location (str): Location for the .json file with the movie data.
        media_id (str): The media you want the income for.

    Returns:
        list[str]: List of the keywords.
    """
    data = load_json(import_location)

    keywords = []
    for i in range(len(data[media_id]["keywords"]["keywords"])):
        keywords.append(data[media_id]["keywords"]["keywords"][i]["name"])
    return keywords
