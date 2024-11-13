import os,requests,pydoc,json,sys
from dotenv import load_dotenv, dotenv_values 

Get_new_data = True #If true, does a API request, if false uses data in data.json
media_list = [] 

if Get_new_data:
    load_dotenv() 
    Auth_key = os.getenv("MOVIEDB_APP_AUTH_DOMAIN")

    #API request 
    #url = "https://api.themoviedb.org/3/authentication"
    url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"

    #TODO: make this only get data if data.json is empty (as to reduce the amount of searches)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer %s" % Auth_key
    }

    response = requests.get(url, headers=headers)
    response_text = json.loads(response.text)
    response_text_formatted = json.dumps(response_text, indent=4)
    if not response_text.get("success", True):
        sys.exit("API conection failed, error: %s\n%s" % (response_text["status_code"],response_text["status_message"]))
        


    with open("data.json", "w") as f:
        f.write(response_text_formatted)
else:
    print("Did not retreve new data, used old data. \n")
    with open("data.json") as f:
        response_text = json.load(f)


data = response_text["results"]

for i in range(0,len(data)):
    if data[i]["adult"]:
        print("is adult")
        media_list.append(data[i]["title"])
    #print(data[i]["title"])

print(media_list)