function generateRandomID(schema, objectType) {
  const randomId = Math.random().toString(36).substring(7);
  return `${schema}.${objectType}_${randomId}`;
}

function generateNode(schema, objectType, level) {
  return {
      id: generateRandomID(schema, objectType),
      schema_name: schema,
      object_name: `${objectType}_${Math.random().toString(36).substring(2, 7)}`,
      object_type: objectType,
      level: level,
      cluster: Math.floor(Math.random() * 3), // Random cluster between 0 and 2
      in_degree: Math.floor(Math.random() * 3), // Random in_degree between 0 and 2
      out_degree: Math.floor(Math.random() * 3), // Random out_degree between 0 and 2
  };
}

function generateEdge(sourceNode, targetNode) {
  return {
      source: sourceNode,
      target: targetNode
  };
}

const schemas = ["dbo", "HumanResources", "Sales", "Finance", "Inventory"];
const objectTypes = ["USER_TABLE", "SQL_STORED_PROCEDURE", "VIEW", "FUNCTION"];
const nodes = [];
const edges = [];

// Generate 50 nodes
for (let i = 0; i < 50; i++) {
  const schema = schemas[Math.floor(Math.random() * schemas.length)];
  const objectType = objectTypes[Math.floor(Math.random() * objectTypes.length)];
  const level = Math.floor(Math.random() * 4); // Random level between 0 and 3

  const node = generateNode(schema, objectType, level);
  nodes.push(node);
}

// Generate 100 edges
for (let i = 0; i < 100; i++) {
  const sourceNode = nodes[Math.floor(Math.random() * nodes.length)].id;
  let targetNode;
  do {
      targetNode = nodes[Math.floor(Math.random() * nodes.length)].id;
  } while (sourceNode === targetNode); // Ensure the source and target are different

  const edge = generateEdge(sourceNode, targetNode);
  edges.push(edge);
}

const data = {
  nodes: nodes,
  edges: edges
};

console.log(JSON.stringify(data, null, 2));
