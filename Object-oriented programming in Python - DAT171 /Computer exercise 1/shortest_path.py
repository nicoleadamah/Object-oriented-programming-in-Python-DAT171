import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from matplotlib.collections import LineCollection
from scipy.sparse.csgraph import shortest_path
from scipy.spatial import cKDTree
import time
import math

# A code written by Nicole Adamah & Sofia Nilsson

# Task 1
def read_coordinate_file(filename):
    """
    :param filename: The input filename receives a file with city coordinates
    :return: returns a numpy array with coordinates without any special signs
    """
    with open(filename) as file:
        coordinates = []
        for line in file:
            a, b = line.strip('{' '}\n').split(',')  # takes out newlines and brackets
            a, b = float(a), float(b)  # a is the latitude, b is the longitude
            x, y = (np.pi * b / 180), np.log(
                np.tan(np.pi / 4 + (np.pi * a) / 360))  # Convert a and b using the Mercator projection
            coordinates.append([x, y])
    return np.array(coordinates)  # converts the coordinates to a numpy array

# Task 2, 5, 7 (all the plots)
def plot_points(coord_list, indices, path):
    """
        :param coord_list: coord_list is the output from the read_coordinate_file
        :param indices: the connections between the points
        :param path: the shortest path from the function find_shortest_path
        :return: returns the plot
        """
    # Separates the coordinates in different arrays
    x = coord_list[:, 1]
    y = coord_list[:, 0]
    plott = plt.scatter(y, x, marker='o', s=10)  # creates a scatter plot from the coordinates in coord_list

    line_segments = LineCollection(coord_list[indices], colors='k', alpha=0.2, linewidths=0.8, zorder=0)  # creates the lines between the points
    plt.gca().add_collection(line_segments)

    x_shortest = coord_list[shortest][:, 1]  # x-coordinates for the shortest path
    y_shortest = coord_list[shortest][:, 0]  # y-coordinates for the shortest path

    plt.axis('equal')
    plt.plot(y_shortest, x_shortest, 'r', zorder=2)  # plots the shortest path
    plt.title('City with coordinates and shortest path')
    plt.show()

    return plott, line_segments

# Task 3
def construction_graph_connections(coord_list, radius):
    """
    :param coord_list: the output from read_coordinate_file
    :param radius: given from the task, the maximum radius between cities
    :return: a numpy array with connections between the cities and the distances between the cities
    """
    distances = []
    connections = []
    radius2 = radius * radius
# This appoints an index to all the cities and then the distance between the cities is calculated
    for i, city_1 in enumerate(coord_list[:-1]):
        for j, city_2 in enumerate(coord_list[i + 1:], i + 1):

            diff2 = (city_1[0] - city_2[0]) ** 2 + (city_1[1] - city_2[1]) ** 2
            # This saves all the distances that are within the given radius then the
            if diff2 <= radius2:
                connections.append([i, j])
                distances.append(math.sqrt(diff2))
    return np.array(connections), np.array(distances)

# Task 4
def construct_graph(indices, distance, N):
    """
    :param indices: a numpy array with the city indices
    :param distance: The second output from construct_graph_connections, the distances
    :param N: the input for the function to know which matrix dimension it is going to create
    :return: the csr-matrix
    """
    row = indices[:, 0]
    col = indices[:, 1]
    # returns a sparse row matrix where each element at index [i, j] in the matrix is the distance between city i and j
    return csr_matrix((distance, (row, col)), shape=(N, N))

# Task 6
def find_shortest_path(graph, start_node, end_node):
    """
    :param graph: The csr matrix from construct_graph
    :param start_node: The first city
    :param end_node: The last city
    :return: The shortest way across the country
    """
    dist_matrix, predecessors = shortest_path(graph, directed=False, indices=start_node, return_predecessors=True)

    last_c = end_node
    shortest = [last_c]
    while predecessors[last_c] != -9999:
        shortest.append(predecessors[last_c])
        last_c = predecessors[last_c]

    return shortest[-1::-1], dist_matrix

# task 9
def construct_fast_graph_connections(coord_list, radius):
    """
    :param coord_list: a numpy array with the coordinates of each city
    :param radius: the maximum radius between the cities
    :return: same output from task 3 but a faster version due to the cKDTree.
    """

    # This class provides an index into a set of points which can be used to  look up the nearest neighbors of any points.
    tree = cKDTree(coord_list)
    # Find all points within distance r of point(s) x
    idx_fast = tree.query_ball_point(coord_list, r = radius)

    connections = []

    for i_city, neighbours in enumerate(idx_fast):
        for j_city in neighbours:
            if j_city >= i_city:
                connections.append(np.array([i_city, j_city]))

    connections = np.array(connections)
    connect = np.array([coord_list[connections[:, 0]], [coord_list[connections[:, 1]]]], dtype=object)
    distance = np.linalg.norm((connect[0]) - (connect[1]), axis=-1)

    return connections, np.array(distance[0])

# Calling on each function in the right order.
if __name__ == "__main__":
    start = time.time()
    # ==================================================================================== #
    coord_list = read_coordinate_file('GermanyCities.txt') # change input file manually
    # ==================================================================================== #
    end = time.time()
    print('read_coordinate_file: %.5f seconds' % (end - start))

    ## The changeable parameters
    r = 0.0025 # change input file manually
    start_node = 1573  # change input file manually
    end_node = 10584 # change input file manually

    # Switch between the fast version and the slow version, uncomment the version of choice
    # ==================================================================================== #
    t10 = time.time()
    con, dist = construct_fast_graph_connections(coord_list, r) # Fast version
    # con, dist = construction_graph_connections(coord_list, r) # Slow version
    t11 = time.time()
    print('construct_graph_connections: %.5f seconds' % (t11 - t10))
    # ==================================================================================== #

    t4 = time.time()
    length = len(dist)
    graph = construct_graph(con, dist, length)
    t5 = time.time()
    print('construction_graph: %.5f seconds ' % (t5 - t4))

    t6 = time.time()
    shortest, dist_matrix = find_shortest_path(graph, start_node, end_node)
    t7 = time.time()
    print('find_shortest_path: %.5f seconds' % (t7 - t6))

    t8 = time.time()
    plot_points(coord_list, con, shortest)
    t9 = time.time()
    print('plot_points: %.5f seconds ' % (t9 - t8))

    print('\nThe shortest way is:', shortest)
    print('The total distance is:', dist_matrix[end_node])