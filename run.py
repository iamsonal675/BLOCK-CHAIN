import hashlib
import json
from time import time
from uuid import uuid4
from urllib.parse import urlparse
import requests
from flask import Flask, jsonify, request

class BLOCKCHAIN:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        self.create_block(previous_hash='1', proof = 0)
        self.difficulty  = 2

    def register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def create_block(self, proof, previous_hash=None):
        block:dict = {
            'index':len(self.chain) + 1,
            'timestamp':time(),
            'transacitons':self.current_transactions,
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
    
    def hash(self, block):
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

    def last_block(self):
        return self.chain[-1] if self.chain else None
    
    def mine_block(self):
        last_block = self.last_block
        last_proof = last_block['proof']
        proof = self.proof_of_work(last_proof)

        previous_hash = self.hash(last_block)
        block = self.create_block(proof, previous_hash)

        return block
    
    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            if block['previous_hash'] != self.hash(last_block):
                return False
            
            last_proof = last_block['proof']
            proof = block['proof']
            if not self.valid_proof(last_proof, proof):
                return False
            
            last_block = block
            current_index += 1

        return True
    
    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

            if new_chain:
                self.chain = new_chain
                return True
            
            return False
        

app = Flask(__name__)

node_identifier = str(uuid4()).replace('-','')
gem_stone_coin = BLOCKCHAIN()

@app.route("/mine",methods=["GET"])
def mine():
    last_block = gem_stone_coin.last_block
    last_proof = last_block['proof']
    proof = gem_stone_coin.proof_of_work(last_proof)

    gem_stone_coin.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    previous_hash = gem_stone_coin.hash(last_block)
    block = gem_stone_coin.create_block(proof, previous_hash)

    response = {
        "message":"New Block Forged",
        "index":block['index'],
        'transactions':block['transactions'],
        'proof':block['proof'],
        'previous_hash': block['previous_hash']
    }

    return jsonify(response), 200

@app.route("/transactions/new",methods=["POST"])
def new_transaction():
    values = request.get_json()

    required = ['sender','recipient','amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    
    index = gem_stone_coin.new_transaction(values['sender'],values['recipient'],values['amount'])
    response = {"message":f"Transaction will be added to Block {index}"}
    return jsonify(response), 201

@app.route("/chain",methods=["GET"])
def full_chain():
    response = {
        'chain':gem_stone_coin.chain,
        "length": len(gem_stone_coin.chain)
    }
    return jsonify(response), 200

@app.route("/nodes/register",methods=["POST"])
def register_nodes():
    values = request.get_json()

    nodes = values.get("nodes")
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400
    
    for node in nodes:
        gem_stone_coin.register_node(node)
    
    response = {
        "message":"New nodes have been added",
        "total_nodes":list(gem_stone_coin.nodes),
    }
    return jsonify(response), 201

@app.route("/nodes/resolve",methods=["GET"])
def consensus():
    replaced = gem_stone_coin.resolve_conflicts()

    if replaced:
        response = {
            "message":"Our chain was replaced",
            "new_chain":gem_stone_coin.chain
        }
    else:
        response = {
            "message":"Our chain is authoritative",
            "new_chain":gem_stone_coin.chain
        }
    
    return jsonify(response), 200

if __name__=="__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p','--port',default=5000, type=int,help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host="0.0.0.0", port=port)