import ast
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

## Network Generator Function
# Network for Mention
def mentionGraph(df):
    df = df[df.mentioned.notnull()]
    print('Data Length:',len(df))
    # Network-X
    G = nx.Graph()
    # Add node-edge
    for user, users_mention in df[['username','mentioned']].to_numpy():
        for user_mention in ast.literal_eval(users_mention):
            G.add_edge(user,user_mention)
    G.edges(data=True)
    return(G)

# Draw Graph
def drawNetwork(G, title=None):
    plt.figure(figsize=(12,6))
    ax = plt.gca()
    if title:
        ax.set_title(title)
    nx.draw(G, with_labels=True, font_size=13, ax=ax)

# Setup Degree Table
def networkDegree(G, dType):
    if dType=='Centrality':
        dg = pd.DataFrame(nx.degree_centrality(G).items(), columns=['Degree Centrality','score'])
    elif dType=='Betweeness':
        dg = pd.DataFrame(nx.betweenness_centrality(G).items(), columns=['Betweeness Centrality','score'])
    elif dType=='Closeneess':
        dg =pd.DataFrame(nx.closeness_centrality(G).items(), columns=['Closeness Centrality','score'])
    return dg

# Plot Degree
def plotDegree(dg, title):
    dg.sort_values(dg.columns[1], ascending=False)[:5].plot.barh(title=title ,x=dg.columns[0], y=dg.columns[1], stacked=True)