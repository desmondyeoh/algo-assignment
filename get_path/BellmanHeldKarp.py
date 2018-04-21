# -*- coding: utf-8 -*-
""" BellmanHeldKarp.py


    Use Bellman-Held-Karp algorithm (a dynamic programming approach) to 
solve for shortest Hamiltonian path. The algorithm is used to solve 
Traveling Salesman Problem which is to find the shortest Hamiltonian 
circuit. Extra node connecting all other vertices with 0 cost is added to 
reduce the circuit found to a path.

References:

    Michael Held and Richard M. Karp. 1961. A dynamic programming approach
        to sequencing problems. In Proceedings of the 1961 16th ACM national 
        meeting (ACM '61). ACM, New York, NY, USA, 71.201-71.204. 
        DOI: https://doi.org/10.1145/800029.808532

    Richard Bellman. 1962. Dynamic Programming Treatment of the Travelling 
        Salesman Problem. J. ACM 9, 1 (January 1962), 61-63.
        DOI=http://dx.doi.org/10.1145/321105.321111
"""
__author__ = "ONG DING SHENG"
__email__ = "sheng970303@gmail.com"
__date__ = "13 April 2018"

import itertools


def hc_modify(matrix, origin=None, destination=None):
	""" | (list[list], Optional: int, int) -> (list[list])
	| 
	| Add nodes to the adjacency matrix based on below conditions:
	| 1. IF without origin and destination, THEN add node that connect every
	|    vertices with 0 cost.
	| 2. IF without destination, THEN add node that connect every vertices
	|    with 0 cost except edge that connects the node and origin with very
	|    negative cost.
	| 3. IF origin and destination are specified, THEN add 1 nodes which is
	|    connected to origin and destination respectively with very negative
	|    cost.
	| 
	| Parameters:
	|     matrix     : distance matrix
	|     origin     : index of origin (default=None)
	|     destination: index of destination vertex (default=None)
	| 
	| Returns:
	|     List[list] : modified distance matrix
	| 
	| Example:
	| >>> matrix = [[0, 1, 2],
	| ...           [1, 0, 3],
	| ...           [2, 3, 0]]
	| >>> hc_modify(matrix)
	| [[0, 0, 0, 0], [0, 0, 1, 2], [0, 1, 0, 3], [0, 2, 3, 0]]
	| >>> hc_modify(matrix, origin=0, destination=2)
	| [[ 0 , -24, inf, inf],
	|  [inf,  0 , 25 , 26 ],
	|  [inf, 25 ,  0 , 27 ],
	|  [-24, 26 , 27 ,  0 ]]
	|
	"""
	if origin == destination and destination != None:
		raise Exception("origin and destination are same")

	sum_of_cost = sum([sum(k) for k in matrix])

	n = len(matrix) + 1
	# add one vertex connected to other vertices with 0 cost
	new_matrix = [[0 for x in range(n)] for y in range(n)] 
	for row in range(n - 1):
		for col in range(n - 1):
			new_matrix[row + 1][col + 1] = matrix[row][col]
	
	# if origin and destination are not specified, return the new matrix
	if origin == None and destination == None:
		return new_matrix
		
	# destination is not specified
	if origin == None and destination != None:
		raise Exception("origin is not specified")
	
	if origin == None or destination == None:
		# make cost of edge between origin and added node very negative
		new_matrix[0][origin + 1] = (2 - n) * sum_of_cost
		for row in range(n - 1):
			for col in range(n - 1):
				if row == col:
					continue
				new_matrix[row + 1][col + 1] += sum_of_cost

		return new_matrix

	# disconnect edges except edges that connected to origin and destination
	new_matrix[0][1:] = [float("inf")] * (n - 1)
	for k in range(1, n - 1):
		new_matrix[k][0] = float("inf")

	# connect to origin and destination with negative cost
	new_matrix[0][origin + 1] = (2 - n) * sum_of_cost
	new_matrix[destination + 1][0] = (2 - n) * sum_of_cost
	for row in range(n - 1):
		for col in range(n - 1):
			if row == col:
				continue	
			new_matrix[row + 1][col + 1] = matrix[row][col] + 2 * sum_of_cost

	return new_matrix


def solve_shortest_path(matrix):
	""" | (list[list]) -> (tuple(tuple(int), int))
	| 
	| Use Bellman-Held-Karp algorithm to solve for shortest hamiltonian 
	| circuit. The first and last '0' (starting node) is omitted to 
	| represent the circuit as hamiltonian path. 
	| 
	| Assumption: Input matrix has performed hc_modify() function such that 
	|             an extra node is appended to be treated as starting point.
	| 
	| Parameters:
	|     matrix    : distance matrix
	| 
	| Returns:
	|     Tuple(int): shortest path
	|     Int       : cost of travelling the path
	| 
	| Example:
	| >>> matrix = [[0, 0, 0, 0],
	| ...           [0, 0, 1, 2],
	| ...           [0, 1, 0, 3],
	| ...           [0, 2, 3, 0]]
	| >>> solve_shortest_path(matrix)
	| ((2, 0, 1), 3)
	|
	"""
	n = len(matrix)

	# map cost of nodes to reach the subset (in bits), included the node it 
	# passed before reaching this subset.
	memory = {}
	# cost from '0' to other nodes
	for k in range(1, n):
		memory[(1 << k, k)] = (matrix[0][k], 0)

	# dynamic programming, memorizing cost needed to reach every nodes
	for size in range(2, n):
		for sub_set in itertools.combinations(range(1, n), size):
			bit_set = sum([1 << k for k in sub_set])
			for k in sub_set:
				# exclude the k from subset of nodes, then find cost to reach
				# k passing through the nodes in exc_set
				exc_set = bit_set & ~(1 << k)
				tmp_set = []
				for m in sub_set:
					if m == k:
						continue
					path_length = memory[(exc_set, m)][0] + matrix[m][k]
					tmp_set.append((path_length, m))
				memory.update({(bit_set, k): min(tmp_set)})

	# sub_set: { 1, 2, 3, ... n - 1} (1...1110) n-bits
	sub_set = 2 ** n - 2
	tmp_set = []
	
	# calculate the path with lowest cost
	for k in range(1, n):
		tmp_set.append((memory[(sub_set, k)][0] + matrix[k][0], k))
	cost, parent = min(tmp_set)
	
	# backtracking the path
	path = []
	for i in range(n - 1):
		path.append(parent)
		tmp_set = sub_set & ~(1 << parent)
		_, parent = memory[(sub_set, parent)]
		sub_set = tmp_set

	return tuple(reversed([k - 1 for k in path])), cost