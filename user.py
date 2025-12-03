import json
import os

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


