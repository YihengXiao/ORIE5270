import numpy as np
import heapq as hq


def recover_path(graph, first, source, destination, Negative_cycle=False):
    cost = 0
    path = []
    pt0 = source
    if Negative_cycle == False:
        pt1 = first[pt0]
        while pt1 != destination:
            pt1 = first[pt0]
            path.append(pt0)
            cost += graph[pt0][pt1]
            pt0 = pt1
        path.append(pt1)
        return (path, cost)
    else:
        pt1 = first[pt0]
        while pt1 not in path:
            pt1 = first[pt0]
            path.append(pt0)
            pt0 = pt1
        path = path[path.index(pt1):]
        path.append(pt1)

        for i in range(len(path) - 1):
            cost += graph[path[i]][path[i+1]]
        return (path, cost)


def load_graph(name_txt_file):
    """
    :param name_txt_file: path of a text file recording a graph
    :return: graph, a dictionary,
    e.g {'a': {'b': 1.0, 'c', 2.0}} represents node 'a' connects to 'b' with weight 1.0
    """
    with open(name_txt_file) as f:
        lines = f.readlines()
        pt = []
        graph = {}
        for line in lines:
            line = line.rstrip('\n')
            if line != '' and line[0] != '(':  # start point of a path
                pt = line
            elif line == '':  # empty line, i.e no path start from pt
                graph[pt] = {}
            elif line[0] == '(':
                weight = {}
                for x in line.split(','):
                    if x[0] == '(':
                        a = x.lstrip('(')
                    elif x[-1] == ')':
                        b = float(x.rstrip(')'))
                        weight[a] = b
                graph[pt] = weight
    return graph


def find_negative_cicles(name_txt_file):
    """
    :param graph: catch output of function load_graph(name_txt_file)
    :return:
    1. If it detects a negative cycle, returns path of the cycle and its length.
    2. else, return [] and None
    """
    graph = load_graph(name_txt_file)
    Augmented_graph = graph
    for node in graph.keys():
        Augmented_graph[node]['sink'] = 1.0
    Augmented_graph['sink'] = {}


    M0 = {node: np.inf for node in Augmented_graph.keys()}
    M0['sink'] = 0.0
    first = {}
    for i in range(1, len(Augmented_graph.keys()) + 1):
        M1 = {}
        for v in Augmented_graph.keys():
            col = []
            for w in Augmented_graph[v].keys():
                hq.heappush(col, (M0[w] + Augmented_graph[v][w], w))
            if len(col) > 0 and M0[v] > col[0][0]:  # update
                M1[v] = col[0][0]
                first[v] = col[0][1]
            else:
                M1[v] = M0[v]
        if i == len(Augmented_graph.keys()):
            for item in M1.items():
                if item[1] < M0[item[0]]:
                    (path, length) = recover_path(graph, first, item[0], M0[item[0]], Negative_cycle=True)
                    return (length, path)
            return (None, [])
        M0 = M1


def find_shortest_path_Bellman(name_txt_file, source, destination):
    """
    :param filename
    :param source: starting point
    :param destination:  end point
    :return:
    """
    graph = load_graph(name_txt_file)
    M0 = {node: np.inf for node in graph.keys()}
    M0[destination] = 0.0
    first = {}
    for i in range(1, len(graph.keys()) + 1):
        M1 = {}
        for v in graph.keys():
            col = []
            for w in graph[v].keys():
                hq.heappush(col, (M0[w] + graph[v][w], w))
            if len(col) > 0 and M0[v] > col[0][0]:  # update
                M1[v] = col[0][0]
                first[v] = col[0][1]
            else:
                M1[v] = M0[v]
        if i == len(graph.keys()):
            if M0[source] < M1[source] or source not in first.keys() or destination not in first.values():
                return (None, [])

            (path, cost) = recover_path(graph, first, source, destination, Negative_cycle=False)
            return (cost, path)
        M0 = M1
