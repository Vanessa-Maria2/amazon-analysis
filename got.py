import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import pandas as pd
import streamlit as st
from IPython.display import display, HTML
import numpy as np
import plotly.graph_objects as go

def graph_full(url):
    G = nx.Graph()

    data = pd.read_csv(url)

    nodes = {}

    database = data[['product_id', 'product_name', 'user_id']].copy()

    database['users'] = database['user_id'].apply(lambda x: x.split(','))

    for i, e in database.iterrows():
        G.add_node(e['product_id'], label=e['product_name'])
        nodes[e['product_id']] = {
            "label": e['product_name'],
            "users": e['users']
        }

    for prod_id, values in nodes.items():
        for filho_prod_id, filho_values in nodes.items():
            if filho_prod_id == prod_id:
                continue

            conectados = len(set(values['users']) & set(filho_values['users']))
            if conectados > 0:
                G.add_edge(prod_id, filho_prod_id, weighted=conectados)

    return G  

  
def get_largest_connected_component(G):
    components = list(nx.connected_components(G))
    largest = max(components, key=len)
    return G.subgraph(largest).copy()

def get_high_degree_subgraph(G, min_degree=5):
    high_degree_nodes = [n for n, d in G.degree() if d >= min_degree]
    return G.subgraph(high_degree_nodes).copy()

def node_centrality(G):
    eigenvector_centrality = nx.eigenvector_centrality(G)
    degree_centrality = nx.degree_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)

    plt.figure(figsize=(12, 10))
    plt.subplot(2, 2, 1)
    plt.bar(eigenvector_centrality.keys(), eigenvector_centrality.values())
    plt.title("Centralidade de Eigenvector")
    plt.xlabel("Nó")
    plt.ylabel("Centralidade")

    plt.subplot(2, 2, 2)
    plt.bar(degree_centrality.keys(), degree_centrality.values())
    plt.title("Centralidade de Grau")
    plt.xlabel("Nó")
    plt.ylabel("Centralidade")

    plt.subplot(2, 2, 3)
    plt.bar(betweenness_centrality.keys(), betweenness_centrality.values())
    plt.title("Centralidade de Betweenness")
    plt.xlabel("Nó")
    plt.ylabel("Centralidade")

    plt.subplot(2, 2, 4)
    plt.bar(closeness_centrality.keys(), closeness_centrality.values())
    plt.title("Centralidade de Closeness")
    plt.xlabel("Nó")
    plt.ylabel("Centralidade")

    plt.tight_layout()
    st.pyplot(plt.gcf())

def visualize_graph(G):
  net = Network(height="600px", width="100%", font_color="black", notebook=True)
  net.barnes_hut()
  net.from_nx(G)

  neighbor_map = net.get_adj_list()

  for node in net.nodes:
    if "title" not in node:
        node["title"] = str(node["id"])
    node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
    node["value"] = len(neighbor_map[node["id"]])

  net.show_buttons(filter_=['physics'])
  net.show("amazonanalysis.html")
  display(HTML('amazonanalysis.html'))
  with open("amazonanalysis.html", "r", encoding="utf-8") as f:
        html_content = f.read()

  metrics(G)
  return html_content

def metrics(G):
  density = nx.density(G)
  esparsy = 1 - density
  assortativity = nx.degree_assortativity_coefficient(G) 
  clustering = nx.average_clustering(G.to_undirected()) 
  clusteringLocal = nx.clustering(G, nodes=['B00J5DYCCA', 'B096MSW6CT'])
  wcc = len(list(nx.connected_components(G)))
  is_directed = G.is_directed()

  st.write(f"**Densidade da rede:** {density:.4f}")
  st.write(f"**Esparsidade da rede:** {esparsy:.4f}")
  st.write(f"**Assortatividade:** {assortativity:.4f}")
  st.write(f"**Coeficiente de clustering global:** {clustering:.4f}")
  for node, value in clusteringLocal.items():
    st.write(f"**Clustering local do nó `{node}`:** {value:.4f}")  
  st.write(f"**Componentes fracamente conectados:** {wcc}")
  st.write(f"**Grafo dirigido:** {is_directed}")


def matrizAdjacencia(G):
    adj_matrix = nx.to_numpy_array(G)
    nodes = list(G.nodes())
    
    df_adjacency = pd.DataFrame(adj_matrix, index=nodes, columns=nodes)
    st.subheader("Matriz de Adjacência")
    st.dataframe(df_adjacency)

def diameterAndPeriphery(G):
    if not nx.is_connected(G):
        componentes = list(nx.connected_components(G))
        maior_componente = max(componentes, key=len)
        G_sub = G.subgraph(maior_componente).copy()
    else:
        G_sub = G

    diameter = nx.diameter(G_sub)
    periphery = nx.periphery(G_sub)

    st.write(f"**Diâmetro:** {diameter}")
    st.write(f"**Periferia:** {periphery}")

    pos = nx.spring_layout(G_sub, seed=42)
    node_colors = ['red' if node in periphery else 'lightblue' for node in G_sub.nodes]

    fig, ax = plt.subplots(figsize=(10, 8))
    nx.draw_networkx_nodes(G_sub, pos, node_color=node_colors, node_size=80, ax=ax)
    nx.draw_networkx_edges(G_sub, pos, alpha=0.3, ax=ax)
    ax.set_title(f"Periferia da Rede (nós vermelhos) - Diâmetro: {diameter}")
    ax.axis('off')
    st.pyplot(fig)

def histogramEmpiricalDistributionDegree(G):
    degrees = [G.degree(node) for node in G.nodes()]
    hist, bins = np.histogram(degrees, bins=10, density=True)

    fig = go.Figure(
        data=[go.Bar(x=bins[:-1], y=hist, marker_color='lightblue', marker_line_color='gray')],
        layout=go.Layout(
            title="Histograma de Distribuição Empírica de Grau",
            xaxis=dict(title="Grau"),
            yaxis=dict(title="Densidade"),
            bargap=0.1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
