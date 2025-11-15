from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from flask_cors import CORS
import json
import os
from datetime import timedelta

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
        if os.path.exists('account_managment.json') :
            try :
                with open('account_managment.json', 'r') as f:
                    return json.load(f)
            except :
                return []

        return []

    def save_user(self) :
        with open('account_management.json', 'w') as file:
            json.dump(self.user_list, file, indent=2)
    
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
        for user in self.user_list:
            if name == user['name']:
                if password == user['password']:
                    return {"success": True}
                else :
                    return {"success": False}
        
        return {"success": False}

temp_user = User()

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)