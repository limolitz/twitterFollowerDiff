#!/usr/bin/env python3


import configparser
import tweepy

def getFollowerDiff():
	api = auth()
	currentFollowers = getAllFollowersUnordered(api)
	oldFollowers = getOldFollowers()
	diff = calcFollowerDiff(oldFollowers,currentFollowers)

def getOldFollowers():
	return set()

def calcFollowerDiff(oldFollowers, currentFollowers):
	newFollowers = currentFollowers.difference(oldFollowers)
	print("{} new followers.".format(len(newFollowers)))
	unfollowers = oldFollowers.difference(currentFollowers)
	print("{} unfollowers.".format(len(unfollowers)))

def getAllFollowersUnordered(api):
	config = getConfig()
	followers = set(api.followers_ids(screen_name=config.get("user", "username")))
	print("You have {} followers.".format(len(followers)))
	return followers

def getConfig():
	config = configparser.ConfigParser()
	config.read('config.ini')
	return config

def auth():
	config = getConfig()
	auth = tweepy.OAuthHandler(config.get("secrets", "consumer_key"), config.get("secrets", "consumer_secret"))
	auth.set_access_token(config.get("secrets", "access_token"), config.get("secrets", "access_token_secret"))

	api = tweepy.API(auth)

	return api

if __name__ == '__main__':
	getFollowerDiff()