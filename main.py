import tweepy

f = open('credentials.txt')
lines = []
for line in f:
    lines.append(line)
f.close

consumer_key = lines[0].strip()
consumer_secret = lines[1].strip()
key = lines[2].strip()
secret = lines[3].strip()


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

api = tweepy.API(auth)
api.update_status('Hello Fellas')