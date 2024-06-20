import hashlib
import json
from time import time

class BLOCKCHAIN:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.create_block(previous_hash='1', proof=0)
        self.difficulty = 2

    def create_block(self, proof, previous_hash=None):
        block:dict = {
            'index':len(self.chain)+1,
            'timestamp':time(),
            'transactions':self.current_transactions,
            'proof':proof,
            'previous_hash':previous_hash or self.hash(self.chain[-1])
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
    
    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof
    
    def valid_proof(self, last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:2] == "0" * self.difficulty
    
    @property
    def last_block(self):
        return self.chain[-1] if self.chain else None
    
    def mine_block(self):
        last_block = self.last_block
        last_proof = last_block['proof']
        proof = self.proof_of_work(last_proof)

        previous_hash = self.hash(last_block)
        block = self.create_block(proof, previous_hash)
        return block
    
if __name__=="__main__":
    gem_coins = BLOCKCHAIN()

    gem_coins.new_transaction("SONAL","VIVEK",1)
    gem_coins.new_transaction("VIVEK","ALSIHA",5)

    gem_coins.mine_block()
    print(json.dumps(gem_coins.chain, indent=2))