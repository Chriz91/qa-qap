from FileParser import FileParser
from dwave_qbsolv import QBSolv
import string


# QBSolv Parameter
# see https://github.com/dwavesystems/qbsolv/blob/master/python/dwave_qbsolv/dimod_wrapper.py for more information
num_repeats = 50
seed = None
algorithm = None
verbosity = 0
timeout = 2592000
solver_limit = None
target = None
find_max = False
solver = 'tabu'

path_to_file = "./datasets/"
file_name = "test_instance.dat"
file_parser = FileParser(path_to_file, file_name)
flows, distances, num_nodes = file_parser.parse_file()

print "Distances", distances
print "Flows", flows
print "Number of nodes", num_nodes

# ToDo: Facility to location mapping. Used for decoding quantum annealing response


# ToDo: Determine length of QUBO matrix and prefactor (QUBO is the matrix in form of a python dictionary)


# ToDo: Fill upper triangular QUBO Matrix


# ToDo: Optimization Function (add distances and flows)
# Add distances


# Add flows


# ToDo: Constraint that every location has exactly one facility assigned 


# ToDo: Constraint that every machine has exactly one location assigned 


# Prints QUBO Matrix to console (for debugging purpose)
# for v in range(0, length_of_QUBO):
#     for j in range(v, length_of_QUBO):
#         print(" %s, %s : %s " % (v, j, QUBO[(v, j)]))

# Call QBSolv
answer = QBSolv().sample_qubo(QUBO, num_repeats=num_repeats, seed=seed, algorithm=algorithm, verbosity=verbosity,
                          timeout=timeout, solver_limit=solver_limit, solver=solver, target=target, find_max=find_max)

# Decode QBSolv answer
samples = list(answer.samples())
print "samples", samples
print "energies", list(answer.data_vectors['energy'])

# ToDo: Decode answer and print it to the console
