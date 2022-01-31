# BlockChain
Learning about Blockchain by building one!

## Hash Functions and it's use
A hash function is a function that takes in an input and outputs a hash value displayed as a hexadecimal number. Hash functions are often used for proving that something is the same as something else, without revealing the information beforehand. The hash values of two inputs that are the same, are always the same, and hence they can be used to prove that the two inputs are equal. Also, the input cannot be revealed since the hash value is displayed as a hexadecimal number.


## Basics of a Blockchain
- A blockchain is an immutable, sequential chain of records called Blocks chained together by hashes.
- Each Block has an index, a timestamp (in Unix time), a list of transactions, a proof, and the hash of the previous Block.
- The hash of the previous block is crucial because it’s what gives blockchains immutability: If an attacker corrupted an earlier Block in the chain then all subsequent blocks will contain incorrect hashes.
