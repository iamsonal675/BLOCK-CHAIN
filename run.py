import hashlib
import json
from time import time

class BLOCKCHAIN:
    def __init__(self):
        self.chain:list = []
        self.current_transactions:list = []
        self.create_block(previous_hash='1',proof=100)

    def create_block(self, proof, previous_hash=None):
        block:dict = {
            "index":len(self.chain) + 1,
            'timestamp':time(),
            'transactions':self.current_transactions,
            'proof':proof,
            'previous_hash':previous_hash or self.hash(self.chain[-1]),
        }

        self.current_transactions = []
        self.chain.append(block)
        return block
    
    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender':sender,
            'recipient':recipient,
            'amount':amount,
        })
        return self.last_block['index'] + 1
    
    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    @property
    def last_block(self):
        return self.chain[-1] if self.chain else None
    

if __name__=="__main__":
    gem_coins = BLOCKCHAIN()

    gem_coins.new_transaction("SONAL","VIVEK",1)
    gem_coins.new_transaction("VIVEK","ALISHA",5)

    last_block = gem_coins.last_block
    last_proof = last_block['proof']
    proof = 123456
    previous_hash = gem_coins.hash(last_block)
    gem_coins.create_block(proof, previous_hash)

    print(json.dumps(gem_coins.chain, indent=2))
