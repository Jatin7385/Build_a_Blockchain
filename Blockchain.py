from time import time
import json
import hashlib
from urllib import response
from uuid import uuid4
import sys

from numpy import block
sys.path.append('c:/users/jatin dhall/anaconda3/lib/site-packages')
from flask import Flask, jsonify, request


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
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]


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


#Instantiate our node
app = Flask(__name__)

#Generating a globally unique id for our node
node_identifier = str(uuid4()).replace("-","")

#Instantiate the blockchain
blockchain = Blockchain()

@app.route('/mine',methods = ['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']

    proof = blockchain.proof_of_work(last_proof)

    #The miner must be receive a reward of 1 coin for finding the proof
    # The sender is considered to be 0, to signify that this node has mined a new coin
    blockchain.new_transaction(
        sender="0",
        recepient=node_identifier,
        amount=1
    )

     # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/transactions/new',methods = ['POST'])
def new_transactions():
    values = request.get_json()

    #Check that the required fields are in the POST'ed Data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    #Create a new transaction
    index = blockchain.new_transaction(values['sender'],values['recepient'],values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain',methods = ['GET'])
def chain():
    response = {
        'chain' : blockchain.chain,
        'length' : len(blockchain.chain)
    }
    return jsonify(response),200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)