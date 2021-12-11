"""
A Python script which generates a JSON file
filled with persons from the FBI's Wanted program
in a format @simonw's csv-diff and git-history can
easily parse.
For documentation on the FBI Wanted API:
* https://www.fbi.gov/wanted/api
* https://api.fbi.gov/docs
"""

import json
from urllib.request import urlopen, Request

URL = "https://api.fbi.gov/@wanted?page={}"

def get_json(url: str):
	request = Request(
		url,
		headers={
			# The API for some reason requires
			# a cURL user-agent...
			"user-agent": "curl/7.68.0",
			"accept": "application/json"
		}
	)

	with urlopen(request) as res:
		return json.load(res)

def get_all_wanted_people():
	page = 1
	body = get_json(URL.format(page))

	items = body["items"]
	yield from items

	total = body["total"]
	total -= len(items)

	while total > 0:
		page += 1
		body = get_json(URL.format(page))

		items = body["items"]
		yield from items

		total -= len(items)

with open("wanted.json", "w") as f:
	json.dump(
		list(get_all_wanted_people()),
		f,
		indent="\t",
	)
