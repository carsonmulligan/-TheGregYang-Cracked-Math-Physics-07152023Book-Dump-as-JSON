import json
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Load the JSON data
with open('cracked_reading_list.json', 'r') as f:
    data = json.load(f)

# Create a graph
G = nx.Graph()

# Add nodes and edges
for book in data:
    title = book['title']
    author = book['author']
    tags = book['tags']  # Changed from 'concepts' to 'tags'

    # Add nodes
    G.add_node(title, node_type='book')
    G.add_node(author, node_type='author')
    G.add_edges_from([(title, author)])

    for tag in tags:  # Changed from 'concept' to 'tag'
        G.add_node(tag, node_type='tag')  # Changed from 'concept' to 'tag'
        G.add_edge(title, tag)

# Set up the plot
plt.figure(figsize=(20, 20))

# Define node colors
color_map = {'book': 'lightblue', 'author': 'lightgreen', 'tag': 'lightcoral'}  # Changed 'concept' to 'tag'
node_colors = [color_map[G.nodes[node]['node_type']] for node in G.nodes()]

# Define node sizes
node_sizes = [3000 if G.nodes[node]['node_type'] == 'book' else 2000 for node in G.nodes()]

# Draw the graph
pos = nx.spring_layout(G, k=0.5, iterations=50)
nx.draw(G, pos, node_color=node_colors, node_size=node_sizes, with_labels=True, font_size=8, font_weight='bold')

# Add a legend
legend_elements = [plt.Line2D([0], [0], marker='o', color='w', label=node_type.capitalize(),
                              markerfacecolor=color, markersize=10)
                   for node_type, color in color_map.items()]
plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))

# Save the graph
plt.tight_layout()
plt.savefig('reading_list_graph.png', dpi=300, bbox_inches='tight')

# Print some statistics
print(f"Number of nodes: {G.number_of_nodes()}")
print(f"Number of edges: {G.number_of_edges()}")

# Print degree centrality for books
book_centrality = {node: centrality for node, centrality in nx.degree_centrality(G).items() if G.nodes[node]['node_type'] == 'book'}
df_centrality = pd.DataFrame.from_dict(book_centrality, orient='index', columns=['Centrality'])
df_centrality = df_centrality.sort_values('Centrality', ascending=False)
print("\nTop 10 books by degree centrality:")
print(df_centrality.head(10))