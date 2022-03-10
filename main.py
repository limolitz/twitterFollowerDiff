#!/usr/bin/env python3
import configparser
import tweepy
import pickle
import os.path
import json
import subprocess

def getFollowerDiff():
	api = auth()
	currentFollowers = getAllFollowersUnordered(api)
	oldFollowers = getOldFollowers()
	diff = calcFollowerDiff(oldFollowers,currentFollowers,api)

	writeDataToMQTT(currentFollowers,diff)
	writeTweet(diff,api)
	storeFollowers(currentFollowers)

def storeFollowers(currentFollowers):
	pickle.dump(currentFollowers, open( "followers.p", "wb" ))

def getOldFollowers():
	if os.path.isfile("followers.p"):
		return pickle.load(open("followers.p", "rb" ))
	else:
		return set()

def getNamesOf(userList,api):
	names = []
	for userId in userList:
		try:
			name = api.get_user(userId).screen_name
			names.append("@{}".format(name))
		except tweepy.TweepError as e:
			if e.api_code == 50:
				names.append("Deleted user, id {}.".format(userId))
				continue
			if e.api_code == 63:
				names.append("Suspended user, id {}.".format(userId))
				continue
			raise e
	return names

def calcFollowerDiff(oldFollowers, currentFollowers,api):
	newFollowers = currentFollowers.difference(oldFollowers)
	newFollowersNames = getNamesOf(newFollowers,api)
	print("{} new followers.".format(len(newFollowers)))
	unfollowers = oldFollowers.difference(currentFollowers)
	print("{} unfollowers.".format(len(unfollowers)))
	unfollowersNames = getNamesOf(unfollowers,api)
	return [newFollowersNames,unfollowersNames]

def writeTweet(diff,api):
	newFollowers = list(diff[0])
	unfollowers = list(diff[1])
	newFollowerText = formatFollowerList(newFollowers,"New follower")
	unfollowerText = formatFollowerList(unfollowers,"New unfollower")
	statusText = None
	if newFollowerText != "":
		if unfollowerText != "":
			statusText = "{}\n{}".format(newFollowerText,unfollowerText)
		else:
			statusText = newFollowerText
	else:
		if unfollowerText != "":
			statusText = unfollowerText
	if statusText is not None:
		try:
			api.update_status(statusText)
		except tweepy.TweepError as e:
			# duplicates can be ignored
			if e.api_code == 187:
				print("Ignoring duplicate tweet'{}'.".format(statusText))
				return
			raise e
		print(statusText)

def formatFollowerList(nameList,basestring):
	statusText = ""
	if len(nameList) != 0:
		# only one account, write directly
		if len(nameList) == 1:
			statusText += "{}: {}".format(basestring,nameList[0])
		else:
			statusText += "{}s:\n".format(basestring)
			for name in nameList:
				statusText += "- {}\n".format(name)
	return statusText

def writeDataToMQTT(currentFollowers,diff):
	newFollowers = list(diff[0])
	unfollowers = list(diff[1])

	config = getConfig()

	mqttObject = {
		"topic": "twitterFollower",
		"name": config.get("user", "username"),
		"measurements": {
			"newFollowers": newFollowers,
			"unfollowers": unfollowers,
			"totalFollowers": len(currentFollowers)
		}
	}

	mqttString = json.dumps(mqttObject)
	print("Writing JSON: {}".format(mqttString))
	sender = subprocess.Popen([config.get("paths", "mqttPath")], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
	output, errors = sender.communicate(mqttString.encode("utf-8"))
	print(output,errors)


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
