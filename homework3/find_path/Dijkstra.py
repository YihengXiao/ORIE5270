import heapq as hq


def load_graph(name_txt_file):
    """
    Input: name_txt_file, route of the graph
    return: graph, a dictionary stores the graph.    
    """
    with open(name_txt_file) as f:
        lines = f.readlines()
        pt = []
        graph = {}
        for line in lines:
            line = line.rstrip('\n\r')
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


def find_shortest_path(name_txt_file, source, destination):
    """
    Input: name_txt_file, name of text file containing the graph
    Input: source, the source point 
    Input: destination, the end point
    Return: (cost, path), cost, the length of the shortest path; path, each node of the shortest path
    """
    graph = load_graph(name_txt_file)
    d = {source: 0.0}
    F = []  # frontier set
    hq.heappush(F, (0.0, source))  # use a heap to facilitate getting the minimum point
    S = set()
    bk = {}
    while F:
        f = hq.heappop(F)
        S.add(f[1])
        for w in graph[f[1]].keys():
            if w not in S and w not in [item[1] for item in F]:  # update d and bk
                d[w] = d[f[1]] + graph[f[1]][w]
                hq.heappush(F, (d[w], w))
                bk[w] = f[1]
            elif d[f[1]] + graph[f[1]][w] < d[w]:
                d[w] = d[f[1]] + graph[f[1]][w]
                bk[w] = f[1]
    if destination not in bk.keys():
        return (None, [])
    else:
        cost = 0
        path = []
        pt1 = destination
        path.append(pt1)
        while pt1 != source:
            pt0 = bk[pt1]
            path.append(pt0)
            cost += graph[pt0][pt1]
            pt1 = pt0
        path = path[::-1]
        return (cost, path)
