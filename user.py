class User:
    '''This class will deal with account creation as well as user login functions.
       In addition we will handle rewards through the user class and maintain a log
       of previous order history'''
    user_list = []

    def __init__(self, name, password):
        self.name = name
        self.__password = password
        self.logedin = False

    def login(self, name, password) :
        for user in self.user_list:
            if name == user['name']:
                if password == user['password']:
                    print("Correct Password")
                    print("Login Successful")
                    self.logedin = True
                    return True
                else :
                    print("Password not found try again")
                    return False
        
        print("Username not found please try agian")
        return False