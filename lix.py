#!/usr/bin/env python
'''
@author: Vikesh Khanna
Lix Tool is a command line interface for the LiX tests and experiments @LinkedIn.
'''

import sys
import urllib2
import json
import re

LIX_ROOT="https://lix.corp.linkedin.com/api/v1"

# Endpoint to search lix test keys
def get_search_url(fabric, search_term):
	return "{0}/{1}/search/?term={2}".format(LIX_ROOT, fabric, search_term)

# Endpoint to get experiment details for a given LiX test key
def get_experiment_url(fabric, key):
	return "{0}/fabrics/{1}/tests/{2}/experiments".format(LIX_ROOT, fabric, key)

def usage():
	help = "./lix.py -f <fabric> <search_term>"
	details_help = "Searches all the LiX tests for the given search_term. The search is a simple substring matching of the search_term within the test key. Returns all the experiments for the matched tests."
	fabric_help = "fabric : Fabric for the LiX test. Example: PROD."
	search_term_help = "search_term : The exact LiX keys or a substring of the LiX keys required."
	return "%s\n%s\n%s\n%s"%(help, details_help, fabric_help, search_term_help)

if __name__== "__main__" :
	fabric = None
	search_term = None

	if len(sys.argv) < 4:
		print("Missing arguments.")
		print(usage())
		sys.exit(1)

	i = 0
	while i < len(sys.argv):
		arg = sys.argv[i]

		# Get the fabric
		if arg == "-f" or arg == "--f":
			fabric = sys.argv[i+1]
			i += 2
		else:
			search_term = arg
			i += 1		

	# Search all valid tests.
	search_url = get_search_url(fabric, search_term)
	print("Searching LiX Keys containing term: {0}.....".format(search_term))
	search_response = urllib2.urlopen(search_url).read()
	search_json = None

	# Extract the actual json
	try:
		match = re.search("^null\((.*?)\);$", search_response)
		search_json = match.group(1)
	except:
		print("Error parsing the search response from LiX API")
		sys.exit(1)

	keys = json.loads(search_json)

	for key in keys:
		print(key)
		experiment_url = get_experiment_url(fabric, key)
		experiment_response = urllib2.urlopen(experiment_url).read()
		
		experiments = json.loads(experiment_response)
	
		for experiment in experiments:
			print(experiment)

