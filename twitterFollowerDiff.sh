#!/bin/bash
cd /home/florin/bin
/usr/local/bin/t set active wasMitNetPi > /dev/null
/usr/local/bin/t followers wasMitNetzen | sort > followers_new.txt
followerDiff=$(/usr/bin/comm -23 followers_new.txt followers.txt)
charCount=${#followerDiff}

if [ $charCount -gt 1 ]; then
	# /bin/echo "New Follower: @$followerDiff"
  fi

followerDiff=$(/usr/bin/comm -13 followers_new.txt followers.txt)
charCount=${#followerDiff}

if [ $charCount -gt 1 ]; then
	/bin/echo "New Unfollower: @$followerDiff"
fi

/bin/mv followers_new.txt followers.txt
