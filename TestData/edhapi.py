import requests

url = "https://ivaee-internet-video-archive-entertainment-v1.p.rapidapi.com/entertainment/search/"

querystring = {"ExternalIdType":"TMDB","ExternalId":"2502","Includes":"Providers"}

headers = {
    'content-type': "application/json",
    'x-rapidapi-host': "ivaee-internet-video-archive-entertainment-v1.p.rapidapi.com",
    'x-rapidapi-key': "93f4b600aemshd9c2d876469f714p1c0cb3jsn18656827b06a"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)