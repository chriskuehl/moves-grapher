#!/usr/bin/env python3
import json
import sys

with open(sys.argv[1]) as f:
	records = [[p[0], float(p[1])] for p in (line.strip().split("\t") for line in f)]
	print(json.dumps(records))
