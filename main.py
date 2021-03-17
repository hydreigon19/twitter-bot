import tweepy
import time
import requests
import urllib.request
import os
import random

#Pull API and Token key from txt
f = open('credentials.txt')
lines = []
for line in f:
    lines.append(line)
f.close

consumer_key = lines[0].strip()
consumer_secret = lines[1].strip()
key = lines[2].strip()
secret = lines[3].strip()

#Twitter Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

api = tweepy.API(auth)

page = 1
#JSON for certain group of images
url = 'https://danbooru.donmai.us/posts.json?tags=favgroup:9167 status:any&limit=10&page=1'

try:
    #url + page number
    jsURL = url
    response = requests.get(jsURL)
    pageTable = response.json()
    #arrayNum = random.randint(0,9)
    arrayNum = 2

    imageSource = pageTable[arrayNum]["file_url"]
    imageURL = imageSource
    print(imageURL)
    
    #if pixiv id is null print source link
    #else sourceURL pixiv link
    validID = str(pageTable[arrayNum]["pixiv_id"])
    
    if validID == "None":
        sourceURL = str(pageTable[arrayNum]["source"])
        print(sourceURL)
    else:
        danbooruURL = "http://danbooru.donmai.us/posts/" + str(pageTable[arrayNum]["id"])
        
        sourceURL = "https://www.pixiv.net/en/artworks/" + str(pageTable[arrayNum]["pixiv_id"])
        print(danbooruURL)
        print(sourceURL)

    #Retrieve image from JSON
    urllib.request.urlretrieve(imageURL, 'image.jpg')

    #Compress image if larger than 5MB
    

    #Tweet content and upload
    #tweetString = "Sauce: " + sourceURL
    #api.update_with_media('image.jpg', status=tweetString)

    #Remove image after
    #os.remove('image.jpg')

except tweepy.error.TweepError:
    print("Unable to upload large image...")