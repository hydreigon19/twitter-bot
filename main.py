import tweepy
import time
import requests
import urllib.request
import os
import random
from PIL import Image

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

#Size and compress functions
def get_file_size_in_bytes(file_path):
    size = os.path.getsize(file_path)
    return size

def convert_to_mb(size_in_bytes):
    return size_in_bytes/(1024*1024)

def compressImage(file, verbose=False):
    picture = Image.open(file)
    picture = picture.convert('RGB')
    picture.save('image.jpg')
    picture.save("image.jpg", optimize = True, quality = 90)
    return

#JSON for certain group of images
#Only put 2 tags in the url
url = 'https://danbooru.donmai.us/posts.json?tags=favgroup:9487 status:any&limit=10&page='


while True:
    try:
        #url and page number
        random.seed()
        jsURL = url + str(random.randint(1,7))

        response = requests.get(jsURL)
        pageTable = response.json()
        arrayNum = random.randint(0,9)

        imageSource = pageTable[arrayNum]["file_url"]
        imageURL = imageSource
        print(imageURL)
        
        #if pixiv id is null print booru link
        #else sourceURL pixiv link
        validID = str(pageTable[arrayNum]["pixiv_id"])
        
        if validID == "None":
            sourceURL = "http://safebooru.donmai.us/posts/" + str(pageTable[arrayNum]["id"])
            print(sourceURL)
        else:
            danbooruURL = "http://safebooru.donmai.us/posts/" + str(pageTable[arrayNum]["id"])
            
            sourceURL = "https://www.pixiv.net/en/artworks/" + str(pageTable[arrayNum]["pixiv_id"])
            print(danbooruURL)
            print(sourceURL)

        #Retrieve image from JSON
        urllib.request.urlretrieve(imageURL, 'image.jpg')

        #Compress image if larger than 5MB
        verbose = False
        file_path = 'image.jpg'
        size = get_file_size_in_bytes(file_path)
        sizeMB = convert_to_mb(size)
        print(sizeMB)
        
        if sizeMB >= 5.00:
            print("Too big. Compressing...")
            compressImage(file_path, verbose)
        
        #Tweet content and upload
        tweetString = "Sauce: " + sourceURL
        api.update_with_media('image.jpg', status=tweetString)

        #Remove image after
        os.remove('image.jpg')

        #Pause script
        time.sleep(900)

    except tweepy.error.TweepError:
        print("Unable to upload image...")
