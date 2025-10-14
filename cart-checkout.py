import user
import food
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
        return sum((item.price * item.quantity) for item in self.items)
    
    def clearCart(self):
        self.items.clear()
        return
