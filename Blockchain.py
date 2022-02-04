from time import time
import json
import hashlib
from urllib import response
from uuid import uuid4
import sys
from urllib.parse import urlparse
import requests

from numpy import block
from sklearn import neighbors
sys.path.append('c:/users/jatin dhall/anaconda3/lib/site-packages')
from flask import Flask, jsonify, request


class Blockchain():
    def __init__(self):
        print("**********************************Initializing Jatin's Blockchain**********************************")
        self.chain = [] #An empty list that stores the blockchain
        self.current_transactions = [] #An empty list that stores all the current transactions occuring in the blockchain

        self.nodes = set()

        #Creating a genesis block
        self.new_block(proof=100, previous_hash=1)

    def register_nodes(self,address):
        url = urlparse(address)
        self.nodes.add(url.netloc)

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
            "recipient" : recepient,
            "amount" : amount
        })

        #Returning the position of the transaction added, which is next to be mined.
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

###########################################CONSENSUS ALGORITHM##############################

    def valid_chain(self,chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print('\n-----------\n')
            
            #Check if the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False
            #Check if the proof of the work is correct
            if not self.is_valid(last_block['proof'],block['proof']):
                return False
            
            last_block = block
            current_index += 1
        
        return True

    def resolve_conflicts(self):
        neighbors = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbors:
            response = requests.get(f'http://{node}/chain')
        
        if response.status_code == 200:
            length = response.json()['length']
            chain = response.json()['chain']

            #Checking if the length of this node's chain is greater than our node's chain
            if length > max_length and self.valid_chain(chain):
                new_chain = chain
                max_length = length

        #Replace our chain if we discover a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True
        return False

##################################################IMPLEMENTING PROOF OF WORK###################################################################
    def proof_of_work(self, prev_proof):
        # Problem : Find a number p that when hashed with the previous block’s solution a hash with 4 leading 
        # 0s is produced.
        proof = 0
        if self.is_valid(proof, prev_proof) == False:
            proof += 1
        return proof

    @staticmethod
    def is_valid(p, p1):
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
    print("Hello")
    print(values)
    #Check that the required fields are in the POST'ed Data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    #Create a new transaction
    index = blockchain.new_transaction(values['sender'],values['recipient'],values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain',methods = ['GET'])
def chain():
    response = {
        'chain' : blockchain.chain,
        'length' : len(blockchain.chain)
    }
    return jsonify(response),200


@app.route('/nodes/register', methods=['GET', 'POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_nodes(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)