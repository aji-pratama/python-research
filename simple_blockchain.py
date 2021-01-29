from time import time
import hashlib
import json


class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.new_block(previous_hash="thisisthefirsthash", proof=100)
        
    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.pending_transactions = []
        self.chain.append(block)
        return block
    
    @property
    def last_block(self):
        return self.chain[-1]
    
    def new_transaction(self, sender, recepient, amount):
        transaction = {
            'sender': sender,
            'recepient': recepient,
            'amount': amount
        }
        self.pending_transactions.append(transaction)
        return self.last_block['index'] + 1
    
    def hash(self, block):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()
        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()
        
        return hex_hash


blockchain = Blockchain()
t1 = blockchain.new_transaction("Haha", "hehe", "1btc")
blockchain.new_block(123)
