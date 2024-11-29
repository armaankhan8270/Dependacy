import json
import networkx as nx

def process_dependency_data(json_data):
    # Parse JSON data
    data = json_data
    nodes = data.get("nodes", [])
    edges = data.get("edges", [])
    
    # Create a graph
    G = nx.DiGraph()
    
    # Process nodes
    for node in nodes:
        node_data = node['data']
        node_id = node_data['id']
        
        # Parse schema name, object name, and object type from the node ID
        parts = node_id.split('.')
        schema_name = parts[0]
        object_name = parts[1]
        object_type = parts[2]
        
        # Add parsed attributes to the node
        G.add_node(node_id, 
                   schema_name=schema_name, 
                   object_name=object_name, 
                   object_type=object_type, 
                   name=node_data['name'])
    
    # Ensure all nodes referenced in edges are in the graph
    for edge in edges:
        edge_data = edge['data']
        source = edge_data['source']
        target = edge_data['target']
        
        # Add missing nodes with default attributes if they don't already exist
        for node_id in [source, target]:
            if node_id not in G.nodes:
                parts = node_id.split('.')
                schema_name = parts[0]
                object_name = parts[1]
                object_type = parts[2]
                G.add_node(node_id, 
                           schema_name=schema_name, 
                           object_name=object_name, 
                           object_type=object_type, 
                           name=node_id)  # Use the ID as the name if no other name is available
        
        # Add edge to the graph
        G.add_edge(source, target)
    
    # Add dependency levels to nodes
    levels = {}
    for node in nx.topological_sort(G):  # Topological sort ensures we process dependencies in order
        if G.in_degree(node) == 0:
            levels[node] = 1
        else:
            levels[node] = max(levels[predecessor] for predecessor in G.predecessors(node)) + 1
        G.nodes[node]['level'] = levels[node]
    
    # Add clusters using modularity-based community detection
    undirected_G = G.to_undirected()  # Modularity works on undirected graphs
    clusters = nx.community.greedy_modularity_communities(undirected_G)
    
    # Map nodes to clusters
    cluster_map = {}
    for cluster_id, cluster_nodes in enumerate(clusters):
        for node in cluster_nodes:
            cluster_map[node] = cluster_id
    
    # Add cluster information to nodes
    for node in G.nodes:
        G.nodes[node]['cluster'] = cluster_map[node]
    
    # Add more features (e.g., node degree, type of dependencies)
    for node in G.nodes:
        G.nodes[node]['in_degree'] = G.in_degree(node)
        G.nodes[node]['out_degree'] = G.out_degree(node)
    
    # Convert back to JSON-compatible structure
    processed_data = {
        "nodes": [
            {
                "id": node,
                "schema_name": G.nodes[node]['schema_name'],
                "object_name": G.nodes[node]['object_name'],
                "object_type": G.nodes[node]['object_type'],
                "level": G.nodes[node]['level'],
                "cluster": G.nodes[node]['cluster'],
                "in_degree": G.nodes[node]['in_degree'],
                "out_degree": G.nodes[node]['out_degree']
            }
            for node in G.nodes
        ],
        "edges": [
            {
                "source": source,
                "target": target
            }
            for source, target in G.edges
        ]
    }
    
    return processed_data
import json

# File path to your JSON file
file_path = "data.json"

# Step 1: Open and read the JSON file
with open(file_path, "r") as file:
    # Step 2: Load the JSON data
    json_data = json.load(file)
    print(json.dumps(json_data, indent=4))

processed_data = process_dependency_data(json_data)

output_file_path = "pre.json"

with open(output_file_path, "w") as output_file:
    json.dump(processed_data, output_file, indent=4)

print(json.dumps(processed_data, indent=4))
