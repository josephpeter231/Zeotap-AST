from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from models import create_rule, combine_rules, evaluate_rule
from database import  insert_rule, get_rule_by_id, get_all_rules, node_to_dict
import logging
from bson import ObjectId

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
client = MongoClient("mongodb+srv://josephpeterjece2021:AJ9Hg6xTtQBUCoGr@cluster1.xaacunv.mongodb.net/zeotap?retryWrites=true&w=majority")
db = client.rule_engine_db

@app.route('/')
def index():
    rules = get_all_rules()
    return render_template('index.html', rules=rules)

@app.route('/create_rule', methods=['POST'])
def create_rule_api():
    rule_string = request.form['rule_string']
    if not rule_string:
        return jsonify({"error": "Rule string is required"}), 400

    rule_ast = create_rule(rule_string)
    if rule_ast is None:
        return jsonify({"error": "Invalid rule format"}), 400

    rule_id = insert_rule(rule_ast, rule_string)
    return jsonify({"rule_id": rule_id, "status": "Rule created successfully"})
 
@app.route('/combine_rules', methods=['POST'])
def combine_rules_api():
    # Check if the request content type is JSON
    if request.is_json:
        data = request.get_json()
        rule_ids = data.get('rule_ids', [])
    else:
        return jsonify({'error': 'Content-Type not supported. Use application/json'}), 415

    rules = []

    for rule_id in rule_ids:
        rule_id = rule_id.strip()  # Remove any whitespace
        if ObjectId.is_valid(rule_id):  # Check if the ObjectId is valid
            rule = get_rule_by_id(ObjectId(rule_id))  # Convert string to ObjectId
            if rule:
                rules.append(rule)
            else:
                app.logger.warning(f"No rule found for ID: {rule_id}")
        else:
            app.logger.error(f"Invalid ObjectId: {rule_id}")

    if not rules:
        return jsonify({'error': 'No valid rules found'}), 400

    # Combine the rules into a single AST
    try:
        combined_ast = combine_rules(rules)
        combined_rule = node_to_dict(combined_ast)  # Convert back to dict
        return jsonify({'combined_rule': combined_rule}), 200
    except Exception as e:
        app.logger.error(f"Error combining rules: {str(e)}")
        return jsonify({'error': str(e)}), 500




@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_api():
    data = request.json  # Expecting JSON input
    rule_id = data.get('rule_id')
    user_data = data.get('user_data')

    # Retrieve the rule's AST from the database
    rule = db.rules.find_one({'_id': ObjectId(rule_id)})

    if not rule:
        return jsonify({"error": "Rule not found"}), 404

    # Evaluate the rule
    ast = rule.get('ast')  # Assuming you store the AST structure under 'ast'
    result = evaluate_rule(ast, user_data)

    # Return the evaluation result as JSON
    return jsonify({"result": result}), 200

if __name__ == "__main__":
    app.run(debug=True)
