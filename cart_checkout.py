import user
import json
import food
from datetime import datetime
'''This class will handle the cart/checkout system and will interact with the user class'''

class Cart:
    def __init__(self, customer ):
        # customer variable is a 'user.py' class object
        self.items = []
        self.customer = customer

    
    def addItem(self, food):
        # food variable is 'foodItem' object
        for existing in self.items:
            if existing.name == food.name:
                existing.quantity += 1
                return
        self.items.append(food)

    def removeItem(self, foodName):
        for existing in self.items:
            if existing.name == foodName:
                self.items.remove(existing)
                return
    
    def total(self):
        return sum((float(item.price) * float(item.quantity)) for item in self.items)
    
    def clearCart(self):
        self.items.clear()
        return

    def save_order_history(self) :
        new_order = {
            "username" : self.customer.name,
            "items" : [
                {
                    "name" : item.name,
                    "price" : float(item.price),
                    "quantity": item.quantity
                }
                for item in self.items
            ],
            "total" : self.total(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        
        with open("order_history.json", "r") as f:
            orders = json.load(f)
        

        orders.append(new_order)

        with open("order_history.json", 'w') as f:
            json.dump(orders, f, indent=2)

        return

    def load_order_history(self) :
        user_orders = []
        with open("order_history.json", 'r') as f :
            orders = json.load(f)

        for order in orders :
            if order.get('username') == self.customer.name :
                user_orders.append(order)

        return user_orders

        

        