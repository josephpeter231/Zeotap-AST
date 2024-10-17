from pymongo import MongoClient
from bson import ObjectId
from models import Node  # Assuming Node class is defined in models.py

# MongoDB connection
client = MongoClient("mongodb+srv://josephpeterjece2021:AJ9Hg6xTtQBUCoGr@cluster1.xaacunv.mongodb.net/zeotap?retryWrites=true&w=majority")
db = client.rule_engine_db
rules_collection = db.rules

# Convert Node to dictionary representation
def node_to_dict(node):
    if node is None:
        return None
    return {
        'type': node.type,
        'value': node.value,
        'left': node_to_dict(node.left),
        'right': node_to_dict(node.right)
    }

# Convert dictionary representation to Node
def dict_to_node(node_dict):
    if node_dict is None:
        return None
    return Node(
        type=node_dict['type'],
        value=node_dict['value'],
        left=dict_to_node(node_dict.get('left')),  # Use .get() to avoid KeyError
        right=dict_to_node(node_dict.get('right'))  # Use .get() to avoid KeyError
    )

# Insert a rule into the database
def insert_rule(rule_ast, rule_string):
    rule_dict = node_to_dict(rule_ast)
    rule_id = rules_collection.insert_one({"ast": rule_dict, "rule_string": rule_string}).inserted_id
    return str(rule_id)

# Get a rule by its ID
def get_rule_by_id(rule_id):
    # Convert string ID to ObjectId
    try:
        rule = rules_collection.find_one({"_id": ObjectId(rule_id)})  # Use ObjectId for query
    except Exception as e:
        print(f"Error retrieving rule: {e}")
        return None
    
    if not rule:
        return None
    
    return dict_to_node(rule["ast"])
def ast_to_string(node):
    if node is None:
        return ''
    if node['type'] == 'operand':
        return node['value']
    left = ast_to_string(node['left'])
    right = ast_to_string(node['right'])
    return f"({left} {node['value']} {right})"

# Get all rules in the database
def get_all_rules():
    rules = rules_collection.find()
    return [{"id": str(rule["_id"]), "rule_string": rule["rule_string"]} for rule in rules]
