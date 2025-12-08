'''Function to test the backend of the website'''
from user import User
import json
import os
from cart_checkout import Cart
from food import Food

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
        _user = User()
        result = _user.login(name=name, password=password)
        if not result["success"] :
            print("Login failed please try again")
            continue
        else :
            cart = Cart(_user)
            while(True) :
                print("""
Menu:
1. See Menu
2. Add to cart
3. Revmove from cart
4. Checkout cart
5. View Order Hisotry
6. Exit """
)
                choice = input("Enter choice: ")
                if choice == "1":
                    with open("menu_list_copy.json", "r") as f:
                        data = json.load(f)

                    print(f"\n===Tuffy's Tacos Menu===\n")

                    for item in data["menu_list"]:
                        print(f"{item['idNum']}. {item['name']} — ${item['price']:.2f}")
                
                elif choice == "2" :
                    item_id = input("Enter which item you would like to add to your cart:")
                    amount = input("How many would you like:")
                    with open("menu_list_copy.json", "r") as f:
                        data = json.load(f)

                    menu_item = None
                    for item in data["menu_list"]:
                        if str(item["idNum"]) == item_id :
                            menu_item = item
                            break
                    if menu_item is None:
                        print("Item invalid, please enter a valid item")
                    else:
                        food_item = Food(
                            name = menu_item["name"],
                            price = menu_item["price"],
                            idNum = menu_item["idNum"],
                            quantity = amount,
                        )
                        cart.addItem(food_item)
                        print(f"Added {amount} {menu_item["name"]} to cart")

                elif choice == "3" :
                    food_name = input("Enter item you would like to remove:")
                    cart.removeItem(food_name)
                    print(f"Removed {food_name} from cart")

                elif choice == "4" :
                    
                    if not cart.items :
                        print("Your cart is empty")
                    else :
                        print("======Cart======")
                        for item in cart.items:
                            print(f"{item.name} x{item.quantity} - ${item.price} per item")
                            total = cart.total()
                    
                        print(f"Total = ${total}")

                    option = input("Would you like to procced with checkout:(Y/N)")
                    if option == "Y" :
                        print("Checkout seccessful!")
                        order = cart.save_order_history()
                        print("Successfully saved order")
                        cart.clearCart()
                    elif option == "N" :
                        print("Checkout Canceled")
                
                elif choice == "5" :
                    print("======Order History======") 
                    orders = cart.load_order_history()

                    if not orders :
                        print("No order history found")
                    else :
                        for order in orders:
                            print(order)


                elif choice == "6" :
                    break

    elif choice == "2":
        name = input("Enter username: ")
        password = input("Enter password: ")
        new_user = User()
        account_created = new_user.create_account(name, password)
        if not account_created:
            continue

    elif choice == "3" :
        break













