from threading import current_thread
import time
import json
import hashlib

class Blockchain():
    def __init__(self):
        print("**********************************Initializing Jatin's Blockchain**********************************")
        self.chain = [] #An empty list that stores the blockchain
        self.current_transactions = [] #An empty list that stores all the current transactions occuring in the blockchain

        #Creating a genesis block
        self.new_block(proof=100, previous_hash=1)

    def new_block(self,proof, previous_hash = None):
        #Each block consists of an index, a UNIX Timestamp, the list of current transactions, the proof, and the hash of the previous block
        block = {
            "index" : len(self.chain) + 1,
            "timestamp" : time(),
            "transactions" : self.current_transactions,
            "proof" : proof,
            "previous_hash" : previous_hash
        }

        #Then we add the block to the chain and empty the list of current transactions, getting it ready for the next block
        self.chain.append(block)
        self.current_transactions = []

        return block 

    def new_transaction(self, sender, recepient, amount):
        #Appending the new transaction to our existing list of transactions

        #Contents of each transaction : sender, recepient, amount
        self.current_transactions.append({
            "sender" : sender,
            "recepient" : recepient,
            "amount" : amount
        })

        #Returning the position of the transaction added, which is next to be mined.
        return len(self.current_transactions) -1


##################################################IMPLEMENTING PROOF OF WORK###################################################################
    def proof_of_work(self, prev_proof):
        # Problem : Find a number p that when hashed with the previous block’s solution a hash with 4 leading 
        # 0s is produced.
        proof = 0
        if self.is_valid(proof, prev_proof) == False:
            proof += 1
        return proof

    @staticmethod
    def is_valid(self, p, p1):
        guess = f'{p}{p1}'.encode()
        hash_val = hashlib.sha256(guess).hexdigest()
        return hash_val[:4] == "0000" # Checking if the leading 4 digits of the hash value are 0000. If so, then it is valid
###############################################################################################################################################

Blockchain()