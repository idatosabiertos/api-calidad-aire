from twitter import *
import os

con_secret= os.environ.get('con_secret')
con_secret_key= os.environ.get('con_secret_key')
token = os.environ.get('token')
token_key = os.environ.get('token_key')

def get_twitts(account):
    t = Twitter(auth=OAuth(token, token_key, con_secret, con_secret_key))
    twitts = t.statuses.user_timeline(screen_name=account)[0:3]
    twitt_list = []
    for  twitt in  twitts:
        twitt_list.append({"text": twitt["text"], "url":get_url(account,twitt)})
    return(twitt_list)

def get_url(account,tweet):
    url = "https://twitter.com/"+account+"/status/"+ str(tweet["id"])
    return url

def get_cities_tweets(account_dictionary):
    city_twitts = {}
    for account in account_dictionary:
        city_twitts[account["city"]] = {"twitts":get_twitts(account["account"]),"account":account["account"]}
    return city_twitts
