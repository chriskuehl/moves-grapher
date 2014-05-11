import datetime
import json
import requests
import urllib.parse

import config

API_DOMAIN = "https://api.moves-app.com/"
API_ENDPOINT = API_DOMAIN + "api/1.1/"
API_OAUTH = API_DOMAIN + "oauth/v1/"

def get_auth_url():
	url = API_OAUTH + "authorize?response_type=code&client_id=CLIENT_ID&scope={}"
	return fill_url(url).format(
		urllib.parse.quote_plus("activity location"))

def get_access_token(code):
	url = API_OAUTH + \
		"access_token?grant_type=authorization_code&code={}&client_id=CLIENT_ID&client_secret=CLIENT_SECRET"
	url = fill_url(url).format(code)

	r = requests.post(url)
	return r.json()["access_token"]

def fill_url(url):
	"""Replaces CLIENT_ID and CLIENT_SECRET with the appropriate URL-encoded
	constants in the given URL.

	Ensure that this function is passed only safe strings containing no user
	input!"""

	replacements = (
		("CLIENT_ID", config.MOVES_CLIENT_ID),
		("CLIENT_SECRET", config.MOVES_CLIENT_SECRET))

	for find, replace in replacements:
		url = url.replace(find, urllib.parse.quote_plus(replace))

	return url

def get_daily_miles(access_token, date):
	url = API_ENDPOINT + "user/summary/daily/{}".format(date.isoformat())
	r = requests.get(url, headers={"Authorization": "Bearer " + access_token})
	json = r.json()
	dist = 0

	for summary in json[0]["summary"]:
		dist += summary["distance"]

	return meters_to_miles(dist)

def meters_to_miles(meters):
	return meters * 0.000621371
