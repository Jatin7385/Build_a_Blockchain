# BlockChain
Learning about Blockchain by building one!

## Hash Functions and it's use
A hash function is a function that takes in an input and outputs a hash value displayed as a hexadecimal number. Hash functions are often used for proving that something is the same as something else, without revealing the information beforehand. The hash values of two inputs that are the same, are always the same, and hence they can be used to prove that the two inputs are equal. Also, the input cannot be revealed since the hash value is displayed as a hexadecimal number.


## Basics of a Blockchain
- A blockchain is an immutable, sequential chain of records called Blocks chained together by hashes.
- Each Block has an index, a timestamp (in Unix time), a list of transactions, a proof, and the hash of the previous Block.
- The hash of the previous block is crucial because it’s what gives blockchains immutability: If an attacker corrupted an earlier Block in the chain then all subsequent blocks will contain incorrect hashes.
- When our blockchain is instantiated, we'll need to seed a genesis block(A block with no predecessors.
- A proof of work algorithm is how new blocks are created or mined on the blockchain. The goal of POW is to find a number that solves a problem. This number must be easy to verify but difficult to find. The question could be "The hash of x*y ends with a 0, and x = 5, find y". Implementing this in Python : 
```python
from hashlib import sha256
x = 5
y = 0  # We don't know what y should be yet...
while sha256(f'{x*y}'.encode()).hexdigest()[-1] != "0":
    y += 1
print(f'The solution is y = {y}')
```
- In bitcoin, the Proof of work algorithm is called Hashcash. It is the algorithm that miners race to solve in order to create new blocks. On solving the algorithm, the miners are rewarded with 1 bitcoin in a transaction
- ### "The problem being used for this blockchain is: Find a number p that when hashed with the previous block’s solution a hash with 4 leading 0s is produced."
