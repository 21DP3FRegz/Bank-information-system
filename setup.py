import os

if not os.path.exists("transactions.txt"):
    with open("transactions.txt", 'w') as file:
        pass
    
if not os.path.exists("accounts.txt"):
    with open("accounts.txt", 'w') as file:
        pass
    
if not os.path.exists("clients.txt"):
    with open("clients.txt", 'w') as file:
        pass
