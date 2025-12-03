from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from flask_cors import CORS
import json
import os
from datetime import timedelta
from cart_checkout import *
from food import Food


app = Flask(__name__)
app.secret_key = 'jh431kj4hk23jh5lk2h34j3kl2h'
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
CORS(app, supports_credentials=True)


class User:
    '''This class will deal with account creation as well as user login functions.
       In addition we will handle rewards through the user class and maintain a log
       of previous order history'''
       
    user_list = []

    def __init__(self) :
        self.user_list = self.load_users()

    def load_users(self) :
        if os.path.exists('account_management.json') :
            try :
                with open('account_management.json', 'r') as f:
                    data = json.load(f)
                    print(f"Successfully loaded from file: {data}")
                    return data
            except Exception as e:
                print(f"Error loading users: {e}")
                return []

        print("No account file found")
        return []

    def save_user(self) :
        with open('account_management.json', 'w') as file:
            json.dump(self.user_list, file, indent=2)
        print(f"Saved {len(self.user_list)} users")
        
    
    def create_account(self, name, password):
        for user in self.user_list:
            if name == user['name']:
                return {"success" : False}
            
        new_user =  {
            "name" : name,
            "password" : password
        }
        self.user_list.append(new_user)
        self.save_user()
        return {"success": True}

    def login(self, name, password) :
        print(f"Login attempt - Username: '{name}', Password: '{password}'")  
        print(f"Current user_list: {self.user_list}")  
        for user in self.user_list:
            print(f"Checking user: {user}")
            if name == user['name']:
                print(f"Username match found!")
                if password == user['password']:
                    print(f"Password match!")
                    return {"success": True}
                else :
                    print(f"Password wrong")
                    return {"success": False}
        print(f"Username not found")  
        return {"success": False}


temp_user = User()
active_carts = {}   
with open('static/menuLists.json') as f:
    MENU_DATA = json.load(f)
MENU_ITEMS = MENU_DATA["menu_list"]


@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/create-account')
def create_account_page():
    return render_template('create-account.html')

@app.route('/')
def index():
    logged_in = session.get('logged_in', False)
    username = session.get('username')
    return render_template("index.html", logged_in=logged_in, username=username)


@app.route('/api/create-account', methods = ['POST'])
def create_account() :
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"success": False}), 400

    result = temp_user.create_account(username, password)

    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 409


@app.route('/api/login', methods = ['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"success": False}), 400

    result = temp_user.login(username, password)

    if result['success'] :
        session.permanent = True
        session['username'] = username
        session['logged_in'] = True
        if username not in active_carts:
         active_carts[username] = Cart(customer=username)

        return jsonify(result), 200
    else :
        return jsonify(result), 401

@app.route('/api/logout', methods=['GET'])
def api_logout():
    session.clear()
    jsonify({"success": True}), 200
    return render_template("index.html")

@app.route('/api/check-session', methods=['GET'])
def check_session():
    '''Check if user is logged in'''
    if 'logged_in' in session and session['logged_in']:
        return jsonify({
            "logged_in": True, 
            "username": session.get('username')
        }), 200
    else:
        return jsonify({"logged_in": False}), 200

@app.route('/menu')
def menu_page() :
    logged_in = session.get('logged_in', False)
    username = session.get('username', '')
    return render_template('menu.html', logged_in=logged_in, username=username)



@app.route('/api/add-to-cart', methods=['POST'])
def add_to_cart():
     
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    username = session['username']
    data = request.get_json()
    item_id = data.get("item_id")

     
    with open('static/menuLists.json') as f:
        menu = json.load(f)["menu_list"]

     
    item = next((i for i in menu if i["idNum"] == item_id), None)

    if not item:
        return jsonify({"success": False, "message": "Item not found"}), 404

     
    food_item = Food(
        name=item["name"],
        price=item["price"],
        idNum=item["idNum"],
        quantity=1
    )

     
    user_cart = active_carts[username]
    user_cart.addItem(food_item)

    return jsonify({
        "success": True,
        "message": f"Added 1 {item['name']} to cart"
    }), 200



@app.route('/cart')
def cart():
    logged_in = session.get('logged_in', False)
    username = session.get('username', '')
    return render_template('cart.html', logged_in=logged_in, username=username)

@app.route('/api/get-cart', methods=['GET'])
def get_cart():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    username = session['username']

    if username not in active_carts:
        return jsonify({"success": False, "items": []})

    cart = active_carts[username]

    items = [{
        "name": item.name,
        "quantity": item.quantity,
        "price": item.price * item.quantity,
        "idNum": item.idNum
    } for item in cart.items]

    return jsonify({"success": True, "items": items})
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)