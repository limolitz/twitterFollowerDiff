# Twitter Follower Diff

This script watches somebody's followers on Twitter and tweets when it detects some differences.

## Setup

Copy the file `config.ini.sample` to `config.ini` and adjust the contents. Set the username as the account you want to watch.

## Usage
### Bare metal

Dependencies:

* Python3
* tweepy

Make a virtualenv `python3 -m venv .`, activate with `source bin/activate` and install the dependecies via `pip install -r requirements.txt`.

Run `twitterFollowerDiff.py` periodically.

### Docker
Build the container. Mount the `config.ini` and the `followers.p`, owned by the UID `1241`, into the container at `/home/tfd/` and run it periodically.

```Bash
docker build -t tfd .;
docker run -it --rm -v $(PWD)/config.ini:/home/tfd/config.ini -v $(PWD)/followers.p:/home/tfd/followers.p --name tfd tfd
```
