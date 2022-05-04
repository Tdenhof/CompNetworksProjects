import pickle 
import pandas as pd
import ast
#Network from Figure 1
testgraph = {
    'u' : 
        {'x': 5,
        'w': 3,
        'v' : 7,
        'y' : -1,
        'z': -1},

    'x' : {
        'u' : 5,
        'w' : 4,
        'v': -1,
        'y' : 7,
        'z' : 9},
    
    'w' : {
        'u' : 3,
        'x' :4,
        'v' : 3,
        'y' : 8,
        'z' : -1},
    
    'v' : {
        'x' : -1,
        'y' : 4,
        'u' : 7,
        'w' : 3 ,
        'z' : -1},
    
    'y' : {
        'x' : 7,
        'u' : -1,
        'z' : 2,
        'w' : 8},
    
    'z' : {
        'x' : 9,
        'y' : 2,
        'w' : - 1,
        'u' : -1,
        'v' : -1}
}

#update values
def UPDATE(graph,source,dest,cost):
    graph[source][dest] = cost
    graph[dest][source] = cost
    return graph
# Find Neighbors for Source Node
# Returns list of neighbors with distances not = -1
def findNeighbors(graph,source):
  keys = []
  temp = graph[source]
  for key in temp:
    if temp[key] != -1:
      keys.append(key)
  return keys

#Method to be able to send any data objects
def encodeData(data):
    return pickle.dumps(data)

#Method to load any recieved Data objects 
def decodeData(data):
    return pickle.loads(data)

def load_config(datacsv):
  df = pd.DataFrame(pd.read_csv(datacsv))
  dic = {}
  for i in range(len(df)):
    row = df.iloc[i]
    tuples = ast.literal_eval(row[1])
    neighbortuples = {}
    for element in tuples:
      neighbortuples[element[0]] = element[1]
    dic[row[0]] = neighbortuples
  return dic
