from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from flask_cors import CORS
import json
import os
from datetime import timedelta
from cart_checkout import *
from food import Food
from user import User


class DummyUser :
    def __init__(self,name) :
        self.name = name

app = Flask(__name__)
app.secret_key = 'jh431kj4hk23jh5lk2h34j3kl2h'
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
CORS(app, supports_credentials=True)

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

@app.route('/order-history')
def order_history():
    logged_in = session.get('logged_in', False)
    username = session.get('username', '')
    return render_template('order-history.html', logged_in=logged_in, username=username)

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
            active_carts[username] = Cart(customer=DummyUser(username))

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

     
    if username not in active_carts:
         
        current_user = next((u for u in temp_user.user_list if u["name"] == username), None)
        if current_user is None:
            return jsonify({"success": False, "message": "User not found"}), 404
         
        active_carts[username] = Cart(customer=DummyUser(username))

     
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
    



@app.route("/api/checkout", methods=["POST"])
def checkout():
    if "username" not in session:
        return jsonify({"success": False, "message": "Not logged in"}), 401

    username = session["username"]

    if username not in active_carts:
        return jsonify({"success": False, "message": "Cart is empty"}), 400

    cart = active_carts[username]

     
    cart.save_order_history()

     
    cart.clearCart()

    return jsonify({"success": True, "message": "Checkout complete!"})



@app.route("/api/order-history")
def api_order_history():
    if "username" not in session:
        return jsonify({"success": False, "message": "Not logged in"}), 403

    username = session["username"]

    current_user = DummyUser(username)

    cart = Cart(customer=current_user)
    history = cart.load_order_history()

    return jsonify({"success": True, "orders": history})



if __name__ == '__main__':
    app.run(debug=True, port=5000)