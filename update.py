#!/usr/bin/env python3
import datetime
import dateutil.parser
import operator
import os
import os.path
import sys

import api

user_details = lambda line: {
	"name": line[0],
	"start_date": dateutil.parser.parse(line[1]).date(),
	"token": line[2]}

with open(sys.argv[1]) as f:
	users = [user_details(line.strip().split("\t")) for line in f]

for user in users:
	print("Updating {}...".format(user["name"]))
	path = user["name"]

	if not os.path.exists(path):
		os.makedirs(path)

	journal_path = os.path.join(path, "journal")
	journal = {}

	if os.path.exists(journal_path):
		with open(journal_path) as f:
			for line in f:
				parts = line.strip().split("\t")
				date = dateutil.parser.parse(parts[0]).date()

				journal[date] = {"date": date, "miles": float(parts[1])}
	
	# update journal with records up to yesterday
	yesterday = datetime.date.today() - datetime.timedelta(1)
	cur = user["start_date"]

	while cur <= yesterday:
		if not cur in journal:
			try:
				journal[cur] = {"date": cur, "miles": api.get_daily_miles(user["token"], cur)}
				print("\t{}: {} miles".format(cur, journal[cur]["miles"]))
			except ValueError as e:
				print("Unable to read from API, skipping {}...".format(cur))

		cur += datetime.timedelta(days=1)

	with open(journal_path, "w") as f:
		for record in sorted(journal.values(), key=operator.itemgetter("date")):
			line = "{}\t{}".format(record["date"].isoformat(), record["miles"])
			print(line, file=f)

print("All users updated.")
