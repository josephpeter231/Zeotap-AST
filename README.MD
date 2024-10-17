# Rule Engine with AST

The Rule Engine Application dynamically evaluates user eligibility based on attributes like age, department, income, and spending habits. It utilizes an Abstract Syntax Tree (AST) to efficiently create, combine, and modify conditional rules.

# Demonstration Video

[Watch Video](Demo_video/demo.mp4)

## **Features**

- Rule Creation : User will be able to add the rules.
- Combine two or more rules.
- Evaluate the rule 
- storage of each rule in database.

## **Technologies Used**
- Programming Language(Python)
- Flask
- Database - MongoDB
- HTML - UI
- Data Representation : Abstract Syntax Tree (AST)
## **Requirements**

- Python 3.8 or later
- Django 5.1 or the latest version
- Django Rest Framework

## **Installation and Setup**

### 1. Clone the repository
- git clone [https://github.com/josephpeter231/Zeotap-AST](https://github.com/josephpeter231/Zeotap-AST)

### 2. Install Dependencies in terminal
- pip install -r requirements.txt


### 3. Start the Server
- `python app.py` (or) `flask run`
  (application can be accessed [http://127.0.0.1:5000/](http://127.0.0.1:5000/))

## Application Features
  - **Create rule:** Use `/create_rule` to create a new rule with logical conditions(POST method).
  - **List Rules:**  View all created rules in Homepage .
  - **Combine Rules:** Combine multiple rules using `/combine_rules` (POST method).
  - **Evaluate Rule:** Evaluate a rule against user data through `/evaluate_rule`, returning whether the criteria are met (POST method).

<!-- ## **Unit Tests**
1. Model: Testing the creation of a post and ensuring slugs are generated correctly
2. Only author can delete own post
- To Run the unit tests run the following commands in terminal
  - python manage.py migrate
  - python manage.py test (for running the testcases) -->
## Screenshots
### Screenshot 1
![Screenshot1](./Screenshots/image.png)

### Screenshot 2
![Screenshot2](./Screenshots/image%20copy.png)




