'''This class will keep track of all the food on the menu as well as assigne an id number to each menu item'''
class food:
    def __init__(self, name, price, idNum):
        self.name = name
        self.price = price
        self.idNum = idNum
    
    foodList = []
    def addFood(food):
        foodList.append(food)
        #add to json file

    drinkList = []
    def addDrink(food):
        foodList.append(food)
        #add to json file
         
