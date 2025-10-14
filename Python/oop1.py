3# Lets make a class
# Atm
# funtions vs methods : methods are functions inside the class
# Methods are called like e.g. L.append(1)

class Atm :

    # init is a constructor : Auto execute when Class object is made
    def __init__(self):
        self.pin=""
        self.balance=0
        print(id(self))
        self.menu()
       
        
    def menu(self):
        user_input=input(""" Hello how would you like to proceed ?
                            ENTER 1 TO CREATE PIN
                            ENTER 2 TO DEPOSIT
                            ENTER 3 TO WITHDRAW
                            ENTER 4 TO CHECK BALANCE
                            ENTER 5 TO EXIT""")
        if user_input=="1":
           self.create_pin() # method of pin creation
            
        elif user_input=="2":
            self.deposit()   # method of deposition
       
        elif user_input=="3":
            self.withdraw()  # method of Withdrawl
        
        elif user_input=="4":
            self.check_balance()  # method of balance check
       
        else:
            print("bye")


    # pin create method
    def create_pin(self):
        self.pin=input("Enter your pin")
        print("Pin Set Succcessfully")

   # deposit method     
    def deposit(self):
        temp=input("Enter your pin")
        if temp==self.pin:
            amount= int( input ("Enter the amount"))
            self.balance=self.balance+amount
            print("Deposit Successful")
        else:
            print("invalid Pin")

    # withdrawing method
    def withdraw(self):

        temp=input("Enter your pin")
        if temp==self.pin:
            amount=int(input("Enter the amount"))
            if amount<self.balance:
                self.balance=self.balance-amount
                print("Operation Successful")
            else:
                print("insufficient Funds")
        else:
            print("invalid pin")

    # balance check method
    def check_balance(self):
        temp=input("Enter your pin")
        if temp==self.pin:
            print("The balance is : ",self.balance)
        else:
            print("Invalid Pin")
            
            
