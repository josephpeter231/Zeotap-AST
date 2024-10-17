function astToExpression(node) {
    if (!node) return '';

    // If the node is an operand (leaf node), just return its value
    if (node.type === 'operand') {
        return node.value;
    }

    // If the node is an operator, recursively process left and right nodes
    if (node.type === 'operator') {
        const leftExpr = astToExpression(node.left);
        const rightExpr = astToExpression(node.right);

        // Return the expression in the format "(left_expr operator right_expr)"
        return `(${leftExpr} ${node.value} ${rightExpr})`;
    }

    return '';
}

// Example usage with your JSON data
const ast = {
    "left": {
        "left": {
            "left": null,
            "right": null,
            "type": "operand",
            "value": "salary"
        },
        "right": {
            "left": null,
            "right": null,
            "type": "operand",
            "value": "50000"
        },
        "type": "operator",
        "value": ">"
    },
    "right": {
        "left": {
            "left": null,
            "right": null,
            "type": "operand",
            "value": "age"
        },
        "right": {
            "left": null,
            "right": null,
            "type": "operand",
            "value": "30"
        },
        "type": "operator",
        "value": ">"
    },
    "type": "operator",
    "value": "AND"
};

const expression = astToExpression(ast);
console.log(expression); // Outputs: "(salary > 50000 AND age > 30)"
