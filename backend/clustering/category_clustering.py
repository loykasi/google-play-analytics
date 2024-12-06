import requests
import pandas as pd
from io import StringIO
from collections import Counter
from itertools import combinations
from datetime import datetime
import networkx as nx
from community import community_louvain

res = requests.get('http://database_api:8000/group/category/7')
df = pd.read_json(StringIO(res.text))

G = nx.Graph()

for category_list in df['categories']:
    for cat1, cat2 in combinations(category_list, 2):  # Pairwise combinations
        if G.has_edge(cat1, cat2):
            G[cat1][cat2]['weight'] += 1  # Increment weight if edge already exists
        else:
            G.add_edge(cat1, cat2, weight=1)

print("Edges with weights:")
for edge in G.edges(data=True):
    print(edge)

# Step 1: Apply the Louvain algorithm
partition = community_louvain.best_partition(G)

# Step 2: Convert the results into a DataFrame
community_df = pd.DataFrame(list(partition.items()), columns=["Category", "Community"])
print(community_df)

# Prepare nodes with community info
nodes = [{"id": node, "group": partition[node]} for node in G.nodes()]

# Prepare edges with weights
links = [
    {"source": edge[0], "target": edge[1], "value": G[edge[0]][edge[1]]["weight"]}
    for edge in G.edges
]

# Combine into graph data
graph_data = {"nodes": nodes, "links": links}

current_day = datetime.now().strftime("%Y-%m-%d")
data = [{
    "updated_date": current_day,
    "clustering_data": graph_data
}]

requests.post("http://database_api:8000/clustering/category", 
    json=data,
    headers={"Content-Type": "application/json"},
)