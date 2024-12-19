import json

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
