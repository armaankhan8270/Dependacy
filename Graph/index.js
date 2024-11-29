document.addEventListener("DOMContentLoaded", () => {
    // Fetch your JSON data
    fetch('data.json')
      .then(response => response.json())
      .then(data => {
        // Initialize Cytoscape
        data={
            "nodes": [
              { "id": "a", "label": "Node A" },
              { "id": "b", "label": "Node B" },
              { "id": "c", "label": "Node C" }
            ],
            "edges": [
              { "source": "a", "target": "b" },
              { "source": "b", "target": "c" },
              { "source": "a", "target": "c" }
            ]
          }
          
        const cy = cytoscape({
          container: document.getElementById('cy'),
          elements: [
            ...data.nodes.map(node => ({ data: { id: node.id, label: node.label } })),
            ...data.edges.map(edge => ({
              data: { source: edge.source, target: edge.target }
            }))
          ],
          style: [
            {
              selector: 'node',
              style: {
                'label': 'data(label)',
                'text-valign': 'center',
                'text-halign': 'center',
                'background-color': '#0074D9',
                'color': '#fff',
                'font-size': '12px',
                'width': 40,
                'height': 40
              }
            },
            {
              selector: 'edge',
              style: {
                'width': 2,
                'line-color': '#999',
                'target-arrow-color': '#999',
                'target-arrow-shape': 'triangle'
              }
            }
          ],
          layout: {
            name: 'cose', // Force-directed layout
            padding: 10
          }
        });
  
        // Add interactivity
        cy.on('tap', 'node', function(evt) {
          const node = evt.target;
          alert(`Clicked on node: ${node.data('label')}`);
        });
      })
      .catch(error => console.error('Error loading data:', error));
  });
  