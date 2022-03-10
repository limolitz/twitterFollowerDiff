# Twitter Follower Diff

This script watches somebody's followers on Twitter and tweets when it detects some differences.

 ## Dependencies

* Python3
* tweepy

Make a virtualenv `python3 -m venv .`, activate with `source bin/activate` and install the dependecies via `pip install -r requirements.txt`.

## Configuration

Copy the file `config.ini.sample` to `config.ini` and adjust the contents. Set the username as the account you want to watch.

## Usage
Run `twitterFollowerDiff.py` periodically.

### Docker
Mount the `config.ini` and the `followers.p`, owned by the UID `1241`, into the container and run it periodically.
