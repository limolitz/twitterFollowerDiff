#!/bin/bash
cd /home/florin/bin
/usr/local/bin/t set active wasMitNetPi >/dev/null 2>/dev/null
if [ $? -eq 0 ]; then
	followersNew=$(/usr/local/bin/t followers wasMitNetzen 2>/dev/null)
	if [ $? -eq 0 ]; then
		echo "$followersNew" | sort > followers_new.txt
		followerDiff=$(/usr/bin/comm -23 followers_new.txt followers.txt)
		charCount=${#followerDiff}

		if [ $charCount -gt 1 ]; then
			if [ $charCount -gt 400 ]; then
				/bin/echo "Error. Too many chars: $charCount" >&2
				wc followers.txt >&2
				wc followers_new.txt >&2
				cp followers.txt followers_bug_$(date "+%s").txt
				cp followers_new.txt followers_new_bug_$(date "+%s").txt
			else
				/bin/echo "New Follower: @$followerDiff"
			fi
		fi

		followerDiff=$(/usr/bin/comm -13 followers_new.txt followers.txt)
		charCount=${#followerDiff}

		if [ $charCount -gt 1 ]; then
			if [ $charCount -gt 400 ]; then
				/bin/echo "Error. Too many chars: $charCount" >&2
				wc followers.txt >&2
        wc followers_new.txt >&2
        cp followers.txt followers_bug_$(date "+%s").txt
				cp followers_new.txt followers_new_bug_$(date "+%s").txt
			else
				/bin/echo "New Unfollower: @$followerDiff"
			fi
		fi

		/bin/mv followers_new.txt followers.txt
	else
		#/bin/echo "Getting followers failed." >&2
		exit 2
	fi
else
	/bin/echo "Setting active user failed." >&2
	exit 1
fi
