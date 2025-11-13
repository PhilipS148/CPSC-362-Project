'''Function to test the backend of the website'''
from user import User
import json
import os

FILENAME = "account_management.json"

if os.path.exists(FILENAME) :
    with open(FILENAME, 'r') as f:
        User.user_list = json.load(f)

while True:
    print("========Tuffy's Tacos========")
    print("""
Menu
1. Login
2. Create Account
3. Exit""")

    choice = input("Enter choice: ") 

    if choice == "1":
        name = input("Enter username: ")
        password = input("Enter password: ")
        _user = User(name, password)
        if not _user.login(name = name, password = password):
            continue
        else :
            while(True) :
                print("""
Menu:
1. See Menu
2. Place Order
3. See Order History
4. Exit """
)
                choice = input("Enter choice: ")
                if choice == "1":
                    with open("menuLists.json", 'r') as f :
                        menu_list = json.load(f)

                    print(menu_list)

                elif choice == "2" :
                    break

                elif choice == "3" :
                    break

                elif choice == "4" :
                    break 
    elif choice == "2":
        name = input("Enter username: ")
        password = input("Enter password: ")
        new_user = User(name, password)
        account_created = new_user.create_account()
        if not account_created:
            continue

    elif choice == "3" :
        break













