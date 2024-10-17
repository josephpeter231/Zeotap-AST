class Node:
    def __init__(self, type, left=None, right=None, value=None):
        self.type = type
        self.left = left
        self.right = right
        self.value = value

def create_rule(rule_string):
    tokens = tokenize(rule_string)
    if not tokens:
        return None

    ast = parse(tokens)
    if not ast:
        return None

    return ast

def combine_rules(rules):
    """
    This function combines a list of rules (ASTs) using the 'AND' operator.
    Each rule is an AST represented as a Node.
    """
    if not rules:
        return None  # Return None if no rules provided

    combined = None
    for rule in rules:
        if combined is None:
            combined = rule  # First rule becomes the root
        else:
            # Combine with the next rule using AND operator
            combined = Node('operator', left=combined, right=rule, value='AND')

    return combined

def node_to_dict(node):
    if node is None:
        return None
    return {
        'type': node.type,
        'value': node.value,
        'left': node_to_dict(node.left),
        'right': node_to_dict(node.right)
    }

def dict_to_node(node_dict):
    if node_dict is None:
        return None
    return Node(
        type=node_dict['type'],
        value=node_dict['value'],
        left=dict_to_node(node_dict['left']),
        right=dict_to_node(node_dict['right'])
    )

def evaluate_ast(node, user_data):
    """
    Recursively evaluates the AST (Abstract Syntax Tree) with the given user data.
    
    :param node: The AST node to evaluate.
    :param user_data: A dictionary containing user data (e.g., {"age": 35, "salary": 60000}).
    :return: The result of the evaluation (True or False).
    """
    if not node:
        return False

    # If the node is an operand, return its value from user_data
    if node['type'] == 'operand':
        return user_data.get(node['value'])

    # If the node is an operator, evaluate its left and right children
    if node['type'] == 'operator':
        left_val = evaluate_ast(node['left'], user_data)
        right_val = evaluate_ast(node['right'], user_data)

        # Apply the operator
        if node['value'] == '>':
            return left_val > right_val
        elif node['value'] == '<':
            return left_val < right_val
        elif node['value'] == '=':
            return left_val == right_val
        elif node['value'].lower() == 'and':
            return left_val and right_val
        elif node['value'].lower() == 'or':
            return left_val or right_val

    return False


def tokenize(rule_string):
    tokens = rule_string.replace('(', ' ( ').replace(')', ' ) ').split()
    return tokens

def parse(tokens):
    if not tokens:
        return None
    token = tokens.pop(0)
    if token == '(':
        left = parse(tokens)
        op = tokens.pop(0)
        right = parse(tokens)
        tokens.pop(0)  # Remove closing parenthesis
        return Node('operator', left=left, right=right, value=op)
    else:
        return Node('operand', value=token)

def evaluate_condition(condition, data):
    key, operator, value = condition.split()
    if key not in data:
        return False
    user_value = data[key]
    if operator == '>':
        return user_value > int(value)
    elif operator == '<':
        return user_value < int(value)
    elif operator == '==':
        return user_value == value
    return False
