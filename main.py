#!/usr/bin/env python3
import configparser
import tweepy
import pickle
import os.path


def getFollowerDiff():
    api = auth()
    currentFollowers = getAllFollowersUnordered(api)
    oldFollowers = getOldFollowers()
    diff = calcFollowerDiff(oldFollowers, currentFollowers, api)

    writeTweet(diff, api)
    storeFollowers(currentFollowers)


def storeFollowers(currentFollowers):
    pickle.dump(currentFollowers, open("followers.p", "wb"))


def getOldFollowers():
    if os.path.isfile("followers.p"):
        return pickle.load(open("followers.p", "rb"))
    else:
        return set()


def getNamesOf(userList, api):
    names = []
    for userId in userList:
        try:
            name = api.get_user(user_id=userId).screen_name
            names.append(f"@{name}")
        except tweepy.errors.NotFound:
            names.append(f"Deleted user, id {userId}.")
        except tweepy.errors.Forbidden:
            names.append(f"Suspended user, id {userId}.")
            continue
    return names


def calcFollowerDiff(oldFollowers, currentFollowers, api):
    newFollowers = currentFollowers.difference(oldFollowers)
    print(f"{len(newFollowers)} new followers.")
    newFollowersNames = getNamesOf(newFollowers, api)

    unfollowers = oldFollowers.difference(currentFollowers)
    print(f"{len(unfollowers)} unfollowers.")
    unfollowersNames = getNamesOf(unfollowers, api)

    return [newFollowersNames, unfollowersNames]


def writeTweet(diff, api):
    newFollowers = list(diff[0])
    unfollowers = list(diff[1])
    newFollowerText = formatFollowerList(newFollowers, "New follower")
    unfollowerText = formatFollowerList(unfollowers, "New unfollower")
    statusText = None
    if newFollowerText != "":
        if unfollowerText != "":
            statusText = f"{newFollowerText}\n{unfollowerText}"
        else:
            statusText = newFollowerText
    else:
        if unfollowerText != "":
            statusText = unfollowerText
    if statusText is not None:
        print(f"Posting to {api.get_settings()['screen_name']}: {statusText}")
        try:
            api.update_status(statusText)
        except tweepy.errors.Forbidden as e:
            print(f"Error {e}")
            if 186 in e.api_codes:
                # TODO: split up into max tweet length
                pass


def formatFollowerList(nameList, basestring):
    statusText = ""
    if len(nameList) != 0:
        # only one account, write directly
        if len(nameList) == 1:
            statusText += f"{basestring}: {nameList[0]}"
        else:
            statusText += f"{basestring}s:\n"
            for name in nameList:
                statusText += f"- {name}\n"
    return statusText


def getAllFollowersUnordered(api):
    config = getConfig()
    username = config.get("user", "username")
    followers = set(api.get_follower_ids(screen_name=username))
    print(f"{username} has {len(followers)} followers.")
    return followers


def getConfig():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


def auth():
    config = getConfig()
    auth = tweepy.OAuth1UserHandler(
        config.get("secrets", "consumer_key"),
        config.get("secrets", "consumer_secret"),
        config.get("secrets", "access_token"),
        config.get("secrets", "access_token_secret")
    )

    api = tweepy.API(auth)

    return api


if __name__ == '__main__':
    getFollowerDiff()
