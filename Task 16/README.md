# Task 16: Introduction to Classes and inheritance

Here we'll implement two classes, with the example of a simple bank account. The following are guidelines rather than instructions, so make the classes as simple or complex as you want.

1. Create class `BasicBankAccount` that has two functions - `deposit()` and `withdraw()`. The class must also store current balance.

2. Create class `BetterBankAccount` that inherits `BasicBankAccount`, but which raises an error (or just shows an error message) if you try to withdraw more money than you have.

    Optionally, you can add a transaction history (stored in a list as a part of the `BetterBankAccount` object)

The file `bank_account.py` contains a basic structure for the classes. There is no `run.py` and he classes are to be imported and used in python console.

Usage/testing example:
```from bank_account import *

account = BetterBankAccount(10)

account.withdraw(2)
account.withdraw(7)
account.deposit(19)
account.withdraw(3)
account.withdraw(6)
account.withdraw(2)
account.withdraw(7)
account.deposit(18)
account.withdraw(4)
account.withdraw(5)

account.history(7)

print("Current balance is {}".format(account.balance))
```