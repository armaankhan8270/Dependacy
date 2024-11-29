from flask import Flask, render_template, jsonify
from collections import defaultdict
import networkx as nx
import json

app = Flask(__name__)

def calculate_levels(nodes, edges):
    # Create adjacency list for reverse graph (parents)
    parents = defaultdict(list)
    for edge in edges:
        parents[edge['target']].append(edge['source'])
    
    # Calculate levels
    levels = {}
    def get_level(node_id):
        if node_id in levels:
            return levels[node_id]
        if not parents[node_id]:
            levels[node_id] = 0
            return 0
        parent_levels = [get_level(parent) for parent in parents[node_id]]
        levels[node_id] = max(parent_levels) + 1
        return levels[node_id]
    
    for node in nodes:
        get_level(node['id'])
    
    return levels

def generate_dag(nodes, edges):
    # Create a directed graph using NetworkX
    G = nx.DiGraph()
    for node in nodes:
        G.add_node(node['id'], label=node['name'], type=node['label'])
    for edge in edges:
        G.add_edge(edge['source'], edge['target'])

    # Apply Sugiyama's layout algorithm for hierarchical graph drawing
    pos = nx.spectral_layout(G)  # Use a layout to spread out nodes
    return G, pos

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/api/graph-data')
def get_graph_data():
    # Sample data representing a complex database schema
    SAMPLE_DATA = {
        "nodes": [
            {"id": "users", "name": "Users", "label": "Base Table"},
            {"id": "products", "name": "Products", "label": "Base Table"},
            {"id": "categories", "name": "Categories", "label": "Base Table"},
            {"id": "orders", "name": "Orders", "label": "Transaction"},
            {"id": "order_items", "name": "Order Items", "label": "Transaction Detail"},
            {"id": "cart", "name": "Shopping Cart", "label": "Transaction"},
            {"id": "cart_items", "name": "Cart Items", "label": "Transaction Detail"},
            {"id": "user_profiles", "name": "User Profiles", "label": "Profile"},
            {"id": "addresses", "name": "Addresses", "label": "User Data"},
            {"id": "payment_methods", "name": "Payment Methods", "label": "User Data"},
            {"id": "inventory", "name": "Inventory", "label": "Product Data"},
            {"id": "price_history", "name": "Price History", "label": "Product Data"},
            {"id": "product_images", "name": "Product Images", "label": "Product Data"},
            {"id": "order_summary", "name": "Order Summary", "label": "Analytics"},
            {"id": "user_activity", "name": "User Activity Log", "label": "Analytics"},
            {"id": "product_views", "name": "Product Views", "label": "Analytics"},
            {"id": "recommendations", "name": "Product Recommendations", "label": "Analytics"},
            {"id": "support_tickets", "name": "Support Tickets", "label": "Support"},
            {"id": "ticket_messages", "name": "Ticket Messages", "label": "Support"},
            {"id": "ticket_history", "name": "Ticket History", "label": "Support"}
        ],
        "edges": [
            {"source": "user_profiles", "target": "users"},
            {"source": "addresses", "target": "users"},
            {"source": "payment_methods", "target": "users"},
            {"source": "products", "target": "categories"},
            {"source": "inventory", "target": "products"},
            {"source": "price_history", "target": "products"},
            {"source": "product_images", "target": "products"},
            {"source": "orders", "target": "users"},
            {"source": "order_items", "target": "orders"},
            {"source": "order_items", "target": "products"},
            {"source": "cart", "target": "users"},
            {"source": "cart_items", "target": "cart"},
            {"source": "cart_items", "target": "products"},
            {"source": "order_summary", "target": "orders"},
            {"source": "user_activity", "target": "users"},
            {"source": "product_views", "target": "products"},
            {"source": "product_views", "target": "users"},
            {"source": "recommendations", "target": "product_views"},
            {"source": "recommendations", "target": "order_items"},
            {"source": "support_tickets", "target": "users"},
            {"source": "ticket_messages", "target": "support_tickets"},
            {"source": "ticket_history", "target": "support_tickets"}
        ]
    }

    # Calculate levels for each node
    levels = calculate_levels(SAMPLE_DATA["nodes"], SAMPLE_DATA["edges"])
    
    # Generate Directed Acyclic Graph (DAG) and apply Sugiyama's layout
    G, pos = generate_dag(SAMPLE_DATA["nodes"], SAMPLE_DATA["edges"])
    
    # Update nodes with calculated levels and layout positions
    nodes_with_levels = SAMPLE_DATA["nodes"].copy()
    for node in nodes_with_levels:
        node["level"] = levels[node["id"]]
        node["position"] = pos.get(node["id"], [0, 0])
    
    # Prepare data for visualization in JSON format
    return jsonify({
        "nodes": nodes_with_levels,
        "edges": SAMPLE_DATA["edges"]
    })

if __name__ == '__main__':
    app.run(debug=True)
