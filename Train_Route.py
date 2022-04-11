'''
@author HaoNi
2022/3/18
'''
import pylab as p
import networkx as nx

#Create a graph
G = nx.DiGraph()
node_links = [("s1", "v8",1),
              ("v8", "v13",1),
              ("v13", "t1",1),
              ("v13", "t2",2),

              ("s2", "v1",2),
              ("v1", "v4",2),
              ("v1", "v5",3),
              ("v4", "v8",1),
              ("v4", "v9",2),
              ("v9", "v14",2),
              ("v9", "v15",3),
              ("v14", "t3",3),

              ("s3", "v2",3),
              ("v2", "v4",2),
              ("v2", "v5",3),
              ("v5", "v10",3),
              ("v5", "v11",4),
              ("v10", "v14",2),
              ("v10", "v15",3),
              ("v15", "t4",4),
              ("v15", "v18",4),

              ("s4", "v2",3),
              ("s4", "v6",4),
              ("v6", "v10",3),
              ("v6", "v11",4),
              ("v11", "v16",4),
              ("v11", "v17",5),
              ("v16", "v18",4),
              ("v18", "t5",5),
              ("v16", "t6",6),

              ("v17", "v19",5),
              ("v19", "t7",5),
              ("v19", "t8",8),
              ("v17", "t9",9)]

# Create a graph
G.add_weighted_edges_from(node_links)


# The route immediately to the right can be obtained by turning the weights to negative numbers.
def inverse_weight(graph):
    copy_graph = graph.copy()
    for node_name, node_weight in copy_graph.edges.items():
        for val in node_weight:
            node_weight[val] = node_weight[val] * (-1)
    return copy_graph

# Get the route immediately to the right
def longest_path(graph, s, t):
    new_graph = inverse_weight(graph)
    lpath = nx.dijkstra_path(new_graph, source=s, target=t)
    return lpath


# Get all nodes of the current graph
def get_all_nodes(graph):
    all_nodes=[]
    for i in graph.nodes.items():
        all_nodes.append(i[0])
    return all_nodes

# Remove elements from another list
def remove_element(allnodes,list1):
    list2=[]
    for i in allnodes:
        if i not in list1:
            list2.append(i)
    return list2

# Lists take intersections
def list_intersection(list1,list2):
    list3 = list(set(list1).intersection(set(list2)))
    return list3

# Lists take merge sets
def list_union(list1,list2):
    list3=list(set(list1).union(set(list2)))
    return list3

# Remove nodes
def remove_nodes(graph,nodeslist):
    copy_graph = graph.copy()
    for i in nodeslist:
        copy_graph.remove_node(i)
    return copy_graph


# Get all nodes of the left network
def get_left_sub_nodes(graph,s,t):
    # left-right
    path1 = longest_path(graph,"s"+str(int(s[1])-1),"t"+str(int(t[1])-1))
    # right-left
    path2 = nx.dijkstra_path(graph, source=s, target=t)
    # intersection
    inter_path = list_intersection(path1,path2)
    # left-left
    path3 = nx.dijkstra_path(graph, "s"+str(int(s[1])-1),"t"+str(int(t[1])-1))
    count = 0
    for i in inter_path:
        if i in path3:
            count += 1
            path3 = nx.dijkstra_path(graph, "s"+str(int(s[1])-1),"t"+str(int(t[1])-1-count))
    sub_nodes = path3

    for i in range(1,int(s[1])):
        for j in range(1,int(t[1])-1):
            if nx.has_path(graph, "s" + str(i), "t" + str(j)) == True:
                left_path = nx.dijkstra_path(graph, source="s"+str(i), target="t"+str(j))
                sub_nodes = list_union(sub_nodes,left_path)
    return sub_nodes


# Get all nodes of the right network
def get_right_sub_nodes(graph,s,t):
    # left-right
    path1 = longest_path(graph,s,t)
    # right-left
    path2 = nx.dijkstra_path(graph, source="s"+str(int(s[1])+1), target="t"+str(int(t[1])+1))
    # intersection
    inter_path = list_intersection(path1,path2)
    # right-right
    path3 = longest_path(graph,"s"+str(int(s[1])+1),"t"+str(int(t[1])+1))
    # union
    uni_path=list_union(inter_path,path3)
    sub_nodes = uni_path
    for i in range(int(s[1])+1,5):
        for j in range(int(t[1])+2,10):
            if nx.has_path(graph, "s" + str(i), "t" + str(j)) == True:
                right_path = longest_path(graph, "s"+str(i), "t"+str(j))
                sub_nodes = list_union(sub_nodes,right_path)
    return sub_nodes


# Get Subnetwork
def get_sub_graph(graph,sub_nodes):
    copy_graph = graph.copy()
    allnodes = get_all_nodes(copy_graph)
    removelist= remove_element(allnodes, sub_nodes)
    sub_graph = remove_nodes(copy_graph ,removelist)
    return sub_graph



# Get parallel lines
# Find the path pair immediately to the right according to the rule
# that the left network is immediately to the right
def get_left_pair(graph):
    all_nodes_left = get_all_nodes(graph)
    startnodes = []
    endnodes = []
    for i in all_nodes_left:
        if i[0] == "s":
            startnodes.append(i)
        if i[0] == "t":
            endnodes.append(i)
    realend = 1
    pair = []
    for i in startnodes:
        for j in endnodes:
            if (nx.has_path(graph, i, j) == True) and int(j[1])>=realend:
                realend = int(j[1])
        pair.append([i,"t"+str(realend)])
    return pair

# Obtaining paths based on path pairs
def get_parallel_left(graph):
    pair=get_left_pair(graph)
    count = 0
    for i in pair:
        path = longest_path(graph, i[0], i[1])
        print ("parallel_path_"+ str(pair.index(i)+1) +" = ")
        print(path)
        count += 1
    return count

#sort list and reverse
def sort_list(list):
    import re
    def sort_key(s):
        kk = re.compile(r'\d+')
        return int(kk.findall(s)[0])
    list.sort(key=sort_key, reverse=True)
    return list

# Get parallel lines
# Based on the rule that the right network is immediately left, find the immediately left path pair
def get_parallel_right(graph,count):
    all_nodes_right = get_all_nodes(graph)
    startnodes = []
    endnodes = []
    for i in all_nodes_right:
        if i[0] == "s":
            startnodes.append(i)
        if i[0] == "t":
            endnodes.append(i)
    startnodes = sort_list(startnodes)
    endnodes = sort_list(endnodes)
    pair = []
    stn = startnodes.copy()
    edn = endnodes.copy()
    alln = all_nodes_right.copy()
    ng = graph.copy()
    # Search from the outside in
    for i in range(len(startnodes)):
        for j in stn:
            for k in edn:
                if (nx.has_path(ng, j, k) == True):
                    haspath_list = longest_path(ng, j, k)
                    print("parallel_path_" + str(count + i + 1) + " = ")
                    print(haspath_list)
                    alln = remove_element(alln, haspath_list)
                    ng = get_sub_graph(graph,alln)
                    realend = int(k[1])
                    break
            pair.append([startnodes[i],"t"+str(realend)])
            break
        stn = []
        edn = []
        for p in alln:
            if p[0] == "s":
                stn.append(p)
            if p[0] == "t":
                edn.append(p)
        stn = sort_list(stn)
        edn = sort_list(edn)

# Find the path in the rest of the network
def get_confirm_route(graph,s,t):
    left_sub_nodes = get_left_sub_nodes(graph, s, t)
    right_sub_nodes = get_right_sub_nodes(graph, s, t)
    copy_graph = graph.copy()
    path1 = remove_element((remove_element(get_all_nodes(G), left_sub_nodes)), right_sub_nodes)
    RG=get_sub_graph(copy_graph, path1)
    confirm_route = nx.dijkstra_path(RG, source = s, target = t)
    print("confirm_route = ")
    print(confirm_route)

# Total functions
def get_all_route(graph,s,t):
    # Get Left Network
    left_sub_nodes = get_left_sub_nodes(graph, s, t)
    lsg = get_sub_graph(graph, left_sub_nodes)
    # Draw the left network

    # Get Right Network
    right_sub_nodes = get_right_sub_nodes(graph, s, t)
    rsg = get_sub_graph(graph, right_sub_nodes)
    draw_figure(rsg)
    # Get Route
    count = get_parallel_left(lsg)
    get_parallel_right(rsg,count)
    get_confirm_route(graph, s, t)

# Draw the graphs
def draw_figure(graph):
    # Format of the diagram
    pos = nx.shell_layout(graph)
    # draw
    nx.draw(graph, pos, with_labels=True)
    p.show()

# Apply functions
get_all_route(G,"s3","t5")


