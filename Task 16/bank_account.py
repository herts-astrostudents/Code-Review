
class BasicBankAccount(object):
    '''
    Basic bank account.
    Can withdraw, deposit, holds current balance.
    Does not validate the amounts, can go negative.
    '''
    def __init__(self, initial_balance=0):
        # initialise the object
        # this function is called when you create the object by running:
        # account = BasicBankAccount(100)
        pass
    

    def deposit(self, amount):
        '''
        Deposit some amount to current balance
        '''
        pass
    

    def withdraw(self, amount):
        '''
        Withdraw some amount from current balance
        '''
        pass



class BetterBankAccount(BasicBankAccount):
    '''
    Basic bank account than the BasicBankAccount.
    Can withdraw, deposit, holds current balance.
    Does not validate the amounts, can go negative.
    '''
    def __init__(self, initial_balance=0):
        # run the init function from BasicBankAccount to set initial balance
        # Can run functions from BasicBankAccount in a similar manner
        BasicBankAccount.__init__(self, initial_balance)
        pass
    

    def deposit(self, amount):
        '''
        Deposit some amount to current balance.
        Must be positive.
        '''
        pass


    def withdraw(self, amount):
        '''
        Withdraw some amount from current balance.
        Must be positive, must not exceed current balance.
        '''
        pass
    

    def history(self, n=5):
        '''
        Print last N entries in the transaction history.
        '''
        pass