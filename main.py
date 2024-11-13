import os,requests,pydoc,json
from dotenv import load_dotenv, dotenv_values 



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
#if response_text["success"]:
#    print("API conection succsesfull")
#else:
#    print("API conection failed, error: %s\n%s" % (response_text["status_code"],response_text["status_message"]))



with open("data.json", "w") as f:
    f.write(response_text_formatted)

print(response_text["page"])