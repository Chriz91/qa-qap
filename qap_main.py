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

# Facility to location mapping. Used for decoding quantum annealing response
facility_to_location = []
for i in range(num_nodes):
    for j in range(1, num_nodes+1):
        facility_to_location.append(string.ascii_uppercase[i] + str(j))

print "Facility to location", facility_to_location

# Determine length of QUBO matrix and prefactor (QUBO is the matrix in form of a python dictionarylength_of_QUBO
length_of_QUBO = num_nodes**2
prefactor = distances.max()* flows.max()*100
QUBO = {}

# Fill upper triangular QUBO Matrix
for v in range(0, length_of_QUBO):
    for j in range(v, length_of_QUBO):
        QUBO[(v,j)] = 0.0

# Optimization Function (add distances and flows)
# Add distances
dist_x = 0
dist_y = 0
for v in range(0, length_of_QUBO):
    for j in range(v, length_of_QUBO):
        if j % num_nodes == 0 and v != j:
            dist_y +=1
        if v % num_nodes == 0 and j ==v and v != 0:
            dist_x +=1
        QUBO[(v,j)] = QUBO[(v,j)] + distances[dist_x][dist_y]

        if j == length_of_QUBO-1:
            dist_y = dist_x
            if v % num_nodes == num_nodes-1:
                dist_y += 1

# Add flows
for v in range(0, length_of_QUBO):
    for j in range(v, length_of_QUBO):
        QUBO[(v, j)] = QUBO[(v, j)] * flows[v % num_nodes][j % num_nodes]

# Constraint that every location has exactly one facility assigned
for v in range(0, length_of_QUBO):
    for j in range(v, length_of_QUBO):
        if v == j:
            QUBO[(v, j)] = QUBO[(v, j)] + (-1.0) * prefactor
        else:
            if j % num_nodes== v % num_nodes:
                QUBO[(v, j)] = QUBO[(v, j)] + (2.0) * prefactor

# Constraint that every machine has exactly one location assigned
for v in range(0, length_of_QUBO):
    for j in range(v, length_of_QUBO):
        if j % num_nodes == 0 and v != j:
            break
        if v == j:
            QUBO[(v, j)] = QUBO[(v, j)] + (-1.0) * prefactor
        else:
            QUBO[(v, j)] = QUBO[(v, j)] + (2.0) * prefactor

# Prints QUBO Matrix to console (for debugging purpose)
# for v in range(0, length_of_QUBO):
#     for j in range(v, length_of_QUBO):
#         print(" %s, %s : %s " % (v, j, QUBO[(v, j)]))

# Call QBSolv
answer = QBSolv().sample_qubo(QUBO, num_repeats=num_repeats, seed=seed, algorithm=algorithm, verbosity=verbosity,
                          timeout=timeout, solver_limit=solver_limit, solver=solver, target=target, find_max=find_max)

# # Decode QBSolv answer
samples = list(answer.samples())
print "samples", samples
print "energies", list(answer.data_vectors['energy'])

# # Decode answer and print it to the console
for i in range(len(samples)):
    print "Solution Nr", i
    print samples[i]
    for j in range(len(samples[0])):
        if samples[i][j] == 1:
            print facility_to_location[j]