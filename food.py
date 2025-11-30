'''This class will keep track of all the food on the menu as well as assigne an id number to each menu item'''
class Food:
    def __init__(self, name, price, idNum, quantity):
        self.name = name
        self.price = float(price)
        self.idNum = idNum
        self.quantity = quantity
    
    foodList = []
    def addFood(food):
        foodList.append(food)
        #add to json file

    drinkList = []
    def addDrink(food):
        foodList.append(food)
        #add to json file
         
