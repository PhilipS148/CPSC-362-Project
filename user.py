import json
import os

class User:
    '''This class will deal with account creation as well as user login functions.'''
       
    user_list = []

    def __init__(self) :
        self.user_list = self.load_users()
        self.name = None
        self.logged_in = False

    # Loads user data from account_management.json file
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

    # Saves user data to account_managment.json  
    def save_user(self) :
        with open('account_management.json', 'w') as file:
            json.dump(self.user_list, file, indent=2)
        print(f"Saved {len(self.user_list)} users")
        
    # Handles account creation
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

    # Handles user login
    def login(self, name, password) :
        print(f"Login attempt - Username: '{name}', Password: '{password}'")  
        print(f"Current user_list: {self.user_list}")  
        for user in self.user_list:
            print(f"Checking user: {user}")
            if name == user['name']:
                print(f"Username match found!")
                if password == user['password']:
                    print(f"Password match!")
                    self.name = name
                    self.logged_in = True
                    return {"success": True}
                else :
                    print(f"Password wrong")
                    return {"success": False}
        print(f"Username not found")  
        return {"success": False}


