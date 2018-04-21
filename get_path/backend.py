# -*- coding: utf-8 -*-
""" backend.py


	Using Google Distant Matrix API to obtain the distance between cities. The 
distance information obtained is used to build the distance matrix. The
shortest hamiltonian path is computed using Bellman-Held-Karp algorithm.
"""
__author__ = "ONG DING SHENG"
__email__ = "sheng970303@gmail.com"
__date__ = "14 April 2018"

import requests
from .BellmanHeldKarp import solve_shortest_path, hc_modify


def build_distance_matrix(locations):
	""" | (dict{str: tuple}) -> (tuple(list[list], dict{int: str}))
	| 
	| Build matrix of distances between every pair of cities. The distance is
	| obtained by calling Google Maps Distance Matrix API. This function also
	| returns a dictionary with the mapping of the indices to the citys'name.
	| 
	| Parameters:
	|     locations     : dictionary of cities with their coordinates
	| 
	| Returns:
	|     List[list]    : distance matrix
	|     Dict{int: str}: dictionary of city and matrix indices mapping
	| 
	| Example:
	| >>> cities = {
	| ...       "University Islam Antarabangsa": (3.2543339,101.727204)
	| ...     , "University Kebangsaan Malaysia": (3.0145569,101.6816473)
	| ...     , "University Putra Malaysia": (2.9916914,101.714096)
	| ...     , "University of Malaya": (3.1201168,101.6521963)
	| ...     , "Unviersity Sains Islam Malaysia": (2.8442094,101.779696)
	| ... }
	| >>> build_distance_matrix(cities)
	| (
	|  [
	|      [0, 37104, 38622, 25024, 64581],
	|      [39895, 0, 15314, 21720, 45543],
	|      [40582, 16247, 0, 24331, 32619],
	|      [26234, 21775, 23294, 0, 49252],
	|      [67020, 45042, 31913, 48845, 0]
	|  ],
	|  {
	|      0: 'University Islam Antarabangsa',
	|      1: 'University Kebangsaan Malaysia',
	|      2: 'University Putra Malaysia',
	|      3: 'University of Malaya',
	|      4: 'Unviersity Sains Islam Malaysia'
	|  }
	| )
	| 
	"""
	place_name = sorted(locations.keys())
	coordinate = [locations[k] for k in place_name]

	origins = "|".join(["{},{}".format(a, b) for a, b in coordinate])
	destinations = origins

	# make API call
	url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
	data = {
		  "origins"      : origins
		, "destinations" : destinations
		, "key"          : "AIzaSyD2iqsJdN8I8yOKM_kliCbtmVncagXrNSc"
	}
	url = url + "&".join(["{}={}".format(k, v) for k, v in data.items()])
	r = requests.post(url)

	dist_info = r.json()

	# build distance matrix
	n = len(locations)
	matrix = [[float("inf") for x in range(n)] for y in range(n)]

	for i in range(n):
		for j in range(n):
			matrix[i][j] = \
			dist_info["rows"][i]["elements"][j]["distance"]["value"]

	return matrix, {k: v for k, v in enumerate(place_name)}


def get_min_path(locations, origin=None, destination=None):
	"""  | (dict{str: tuple}, Optional: int, int) -> (tuple(list, int))
	|
	| Return shortest hamiltonian passing through all the cities in given
	| locations and the cost to travel through the path in meters (m).
	| 
	| Example:
	| >>> cities = {
	| ...       "University Islam Antarabangsa": (3.2543339,101.727204)
	| ...     , "University Kebangsaan Malaysia": (3.0145569,101.6816473)
	| ...     , "University Putra Malaysia": (2.9916914,101.714096)
	| ...     , "University of Malaya": (3.1201168,101.6521963)
	| ...     , "Unviersity Sains Islam Malaysia": (2.8442094,101.779696)
	| ... }
	| >>> get_min_path(cities)
	| (
	|  [
	|      'University Islam Antarabangsa', 'University of Malaya',
	|      'University Kebangsaan Malaysia', 'University Putra Malaysia',
	|      'Unviersity Sains Islam Malaysia'
	|  ],
	|  94732
	| )
	| 
	"""
	matrix, mapping = build_distance_matrix(locations)

	if origin != None:
		origin = sorted(locations.keys()).index(origin)
	if destination != None:
		destination = sorted(locations.keys()).index(destination)

	matrix = hc_modify(matrix, origin=origin, destination=destination)
	path, cost = solve_shortest_path(matrix)


	return [mapping[k] for k in path], cost