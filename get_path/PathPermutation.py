# -*- coding: utf-8 -*-
""" PathPermutation.py

    Find the shortest hamiltonian path with given list of cities by 
permuting all the vertices to try all possible path. Find the cost of each 
path and record all the path with minimum cost.
"""
__author__ = "ONG DING SHENG"
__email__ = "sheng970303@gmail.com"
__date__ = "13 April 2018"

import itertools


def solve_shortest_path(arg):
	""" | (list[list]) -> (tuple(list[tuple(int)], int))
	|
	| Return all the shortest paths in a list and the cost of the shortest 
	| paths found by permuting every vertices.
	| 
	| Parameters:
	| arg             : distance matrix
	| 
	| Returns:
	| List[tuple(int)]: all possible minimum path
	| Int             : cost of travelling the path
	| 
	| Example:
	| >>> graph = [[0, 1, 2],
	| ...          [1, 0, 3],
	| ...          [2, 3, 0]]
	| >>> solve_shortest_path()
	| ([(1, 0, 2), (2, 0, 1)], 3)
	|
	"""
	shortest_path = []
	min_cost = float("inf")
	# permute all vertex to try all possible path
	for path in itertools.permutations(range(len(arg))):
		cost_of_curr_path = 0
		# calculate path cost
		for k in range(1, len(path)):
			cost_of_curr_path = cost_of_curr_path + arg[path[k - 1]][path[k]]
		# add the shortest path with minimum cost
		if cost_of_curr_path < min_cost:
			shortest_path = [path]
			min_cost = cost_of_curr_path
		elif cost_of_curr_path == min_cost:
			shortest_path.append(path)
		
	return shortest_path, min_cost