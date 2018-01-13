# Twitter Follower Diff

This script watches you followers on Twitter and tweets and posts to an MQTT broker when it detects some differences. For the MQTT script see
 [here](https://github.com/wasmitnetzen/mqttsend).

 ## Dependencies

* Python3
* tweepy

Make a virtualenv `python3 -m venv .`, activate with `source bin/activate` and install the dependecies via `pip install -r requirements.txt`.

## Configuration

Copy the file `config.ini.sample` to `config.ini` and adjust the contents.

## Usage
Either run `twitterFollowerDiff.py` or `cron.sh`.
