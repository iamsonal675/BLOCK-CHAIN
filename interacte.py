import requests
import json

def mine_block(node):
    response = requests.get(f'http://{node}/mine')
    print(response.json())

def new_transaction(node, sender, recipient, amount):
    transaction = {
        "sender": sender,
        "recipient": recipient,
        "amount": amount
    }
    response = requests.post(f'http://{node}/transactions/new', json=transaction)
    print(response.json())

def view_chain(node):
    response = requests.get(f'http://{node}/chain')
    print(response.json())

def register_node(node, new_node):
    nodes = {"nodes": [new_node]}
    response = requests.post(f'http://{node}/nodes/register', json=nodes)
    print(response.json())

def resolve_conflicts(node):
    response = requests.get(f'http://{node}/nodes/resolve')
    print(response.json())

if __name__ == "__main__":
    node_address = 'localhost:5000'
    mine_block(node_address)
    new_transaction(node_address, 'address1', 'address2', 5)
    view_chain(node_address)
    register_node(node_address, 'http://localhost:5001')
    resolve_conflicts(node_address)
