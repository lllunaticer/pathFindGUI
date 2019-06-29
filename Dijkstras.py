# Dijstras算法
def find_lowest_cost(costs,to_process):
    lowest_cost_node = to_process[0]
    lowest_cost = costs[lowest_cost_node]
    if len(to_process)>1:
        for node in to_process[1:]:
            new_cost = costs[node]
            if new_cost < lowest_cost:
                lowest_cost = new_cost
                lowest_cost_node = node
    return lowest_cost_node


def set_up_graph(N,w):
    graph = {}
    for i in range(N):
        graph[i] = {}
    for i in range(N):
        for li in w:
            if(i == li[0]):
                graph[i][li[1]] = li[2]
                graph[li[1]][i] = li[2]
    return graph


def initialize_costs_n_fathers(graph,start):
    costs, fathers ={},{}
    for node in graph:
        if node is start:
            costs[node] = 0
            fathers[node] = None
        else:
            costs[node] = float('inf')
            fathers[node] = None
    return costs,fathers


def get_shortest_path(fathers,start,end):
    path = []
    result = []
    father = end
    path.append(father)
    while father != start:
        father = fathers[father]
        path.append(father)
    for i in range(len(path)-1,-1,-1):#逆序保存路径
        result.append([path[i],path[i-1]])
    result.pop()#删除最后一个list
    return result


def Dijkstras(N,w,start,end):
    graph = set_up_graph(N,w)
    costs, fathers = initialize_costs_n_fathers(graph,start)
    to_process = [i for i in graph.keys()]
    # to_process.remove(end)
    while to_process:
        node = find_lowest_cost(costs,to_process)
        neighbors = graph[node]
        for neighbor in neighbors:
            new_cost = costs[node] + graph[node][neighbor]
            if new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                fathers[neighbor] = node
        to_process.remove(node) # keys donnot share names
    result = get_shortest_path(fathers,start,end)
    return result, costs[end]

