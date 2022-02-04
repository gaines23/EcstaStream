import requests

url = "https://gowatch.p.rapidapi.com/lookup/title/tmdb_id"

querystring = {"id":"496243","type":"movie","country":"us"}

payload = "id=496243&type=movie&country=us"
headers = {
    'content-type': "application/x-www-form-urlencoded",
    'x-rapidapi-host': "gowatch.p.rapidapi.com",
    'x-rapidapi-key': "93f4b600aemshd9c2d876469f714p1c0cb3jsn18656827b06a"
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.text)