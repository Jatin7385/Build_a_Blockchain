class Blockchain():
    def __init__(self):
        print("Jatin's Blockchain")
        self.chain = [] #An empty list that stores the blockchain
        self.transactions = [] #An empty list that stores all the transactions occuring in the blockchain

    def new_block(self):
        pass

    def new_transaction(self, sender, recepient, amount):
        #Appending the new transaction to our existing list of transactions

        #Contents of each transaction : sender, recepient, amount
        self.transactions.append({
            "sender" : sender,
            "recepient" : recepient,
            "amount" : amount
        })

        #Returning the position of the transaction added, which is next to be mined.
        return len(self.transactions) -1
    

Blockchain()