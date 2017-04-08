# Linkybot

## Prerequisites

This bot is written in Python 3. You will need `praw` v4.4.0 to run it.

## Setup

Save the `praw.ini.example` file as `praw.ini` and follow the instructions in
there:

1. `client_id` and `client_secret` for your bot can be obtained on Reddit.com
   by going to Preferences -> Apps and creating a new app.
2. Enter your bot's Reddit username and password to log in.
3. Change the configuration section ([MyBot]) to match your bot's username.
4. Go to `Linkerbot.py`, line 92, and change 'MyBot' to match your bot's
   username.

## Run it

(Make sure Linkybot.py is executable and you are in the right directory.)

```
$ ./Linkybot.py
```
