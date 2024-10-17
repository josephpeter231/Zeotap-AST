class Node:
    def __init__(self, type, left=None, right=None, value=None):
        self.type = type
        self.left = left
        self.right = right
        self.value = value

def tokenize(rule_string):
    import re
    # Tokenize the string while keeping numbers, strings, and operators separate
    tokens = re.findall(r'\w+|==|!=|>=|<=|[><()]|\'[^\']+\'', rule_string)
    return tokens

def parse(tokens):
    if not tokens:
        return None

    token = tokens.pop(0)

    if token == '(':
        # Parse the left operand
        left = parse(tokens)
        # Parse the operator
        op = tokens.pop(0)
        # Parse the right operand
        right = parse(tokens)
        # Remove the closing parenthesis
        tokens.pop(0)
        return Node('operator', left=left, right=right, value=op)
    
    # If it's a number or a string, treat it as an operand
    if token.isdigit():
        return Node('operand', value=int(token))  # Convert numbers to int
    elif token.startswith("'") and token.endswith("'"):
        return Node('operand', value=token.strip("'"))  # Remove quotes for strings
    else:
        return Node('operand', value=token)  # Treat as a regular operand (like 'salary')

def node_to_dict(node):
    if node is None:
        return None
    return {
        'type': node.type,
        'value': node.value,
        'left': node_to_dict(node.left),
        'right': node_to_dict(node.right)
    }

def evaluate_rule(ast, data):
    """
    This function evaluates the AST (Abstract Syntax Tree) of a rule against user data.
    """
    # Base case: if the node is an operand (leaf node), return the corresponding value from the user data
    if ast['type'] == 'operand':
        # If the value is a string (attribute name), get the corresponding value from data
        if isinstance(ast['value'], str) and ast['value'] in data:
            return data[ast['value']]
        return ast['value']  # Return the operand value directly if it's not a variable

    # Recursively evaluate the left and right nodes
    left_value = evaluate_rule(ast['left'], data)
    right_value = evaluate_rule(ast['right'], data)

    # Perform the operation based on the operator in the current node
    if ast['type'] == 'operator':
        operator = ast['value']

        # Ensure left_value and right_value are not None before comparison
        if left_value is None or right_value is None:
            return False  # Return False if we cannot compare due to missing values

        # Handling comparison operators
        if operator == '>':
            return left_value > right_value
        elif operator == '<':
            return left_value < right_value
        elif operator == '==':
            return left_value == right_value
        elif operator == '!=':
            return left_value != right_value

        # Logical AND operator
        elif operator == 'AND':
            return bool(left_value) and bool(right_value)

        # Logical OR operator
        elif operator == 'OR':
            return bool(left_value) or bool(right_value)

    # Return False for invalid operations
    return False

# Example usage
rule_string = "(salary > 50000 OR experience > 5)"
tokens = tokenize(rule_string)

ast = parse(tokens)
print("AST (Node Representation):")
print(node_to_dict(ast))

# User data to evaluate against
user_data = {
    "age": 20,
    "department": "Marketing",
    "salary": 0000,
    "experience": 0
}

result = evaluate_rule(node_to_dict(ast), user_data)
print("Evaluation Result:", result)  # Should print True
