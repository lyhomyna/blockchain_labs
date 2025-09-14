import hashlib
import json

from time import time
from flask import Flask, jsonify, request
from uuid import uuid4

class Blockchain(object):
    def __init__(self):
        self.chain_LMG = []
        self.current_transactions_LMG = []

        genesis_hash = hashlib.sha256("Lyhomyna".encode()).hexdigest()
        self.new_block_LMG(previous_hash=genesis_hash, proof=7092003)

    def new_block_LMG(self, proof, previous_hash=None):
        """
        New block creation

        :param proof: <int> Proof of work
        :param previous_hash: Previous block hash
        :return: <dict> New block
        """

        merkle_root = self.generate_merkle_root(self.current_transactions_LMG)

        block = {
            'index': len(self.chain_LMG) + 1,
            'timestamp': time(),
            'merkle_root': merkle_root,
            'transactions': self.current_transactions_LMG,
            'proof': proof,
            'previous_hash': previous_hash or self.hash_LMG(self.chain_LMG[-1]),
        }

        # Clear mempool
        self.current_transactions_LMG = []

        # Append created block to the chain
        self.chain_LMG.append(block)

        return block

    def new_transaction_LMG(self, sender, recipient, amount):
        """
        Sends a new transaction to the next block

        :param sender: <str> Sender address
        :param recipient: <str> Recipient address
        :param amount: <int> Sum
        :return: <int> Block index, which will store this transaction
        """
        self.current_transactions_LMG.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block_LMG['index'] + 1

    @staticmethod
    def hash_LMG(data_object):
        """
        Creates SHA-256 hash
        :param block: <dict> Block
        :return: <str> hashsum
        """

        block_string = json.dumps(data_object, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @staticmethod
    def generate_merkle_root(transactions):
        if not transactions:
            return hashlib.sha256("".encode()).hexdigest()

        leaves = [Blockchain.hash_LMG(tx) for tx in transactions]

        while len(leaves) > 1:
            if len(leaves) % 2 != 0:
                leaves.append(leaves[-1])

            new_lvl = []
            for i in range(0, len(leaves), 2):
                combined_hash = hashlib.sha256(f'{leaves[i]}{leaves[i+1]}'.encode()).hexdigest()
                new_lvl.append(combined_hash)

            leaves = new_lvl

        return leaves[0]

    @property
    def last_block_LMG(self):
        return self.chain_LMG[-1]

    def proof_of_work_LMG(self, last_proof):
        """
        :param last_proof: <int>
        :return: <int>
        """
        proof = 0
        while self.valid_proof_LMG(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof_LMG(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[-2:] == "09"



app = Flask(__name__)

node_identifier = str(uuid4()).replace('-','')

blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block_LMG
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work_LMG(last_proof)

    blockchain.new_transaction_LMG(
        sender="0",
        recipient=node_identifier,
        amount=1
    )

    previous_hash = blockchain.hash_LMG(last_block)
    block = blockchain.new_block_LMG(proof, previous_hash)
    response = {
        'message':"New Block Forged",
        'index':block['index'],
        'transactions':block['transactions'],
        'proof':block['proof'],
        'previous_hash':block['previous_hash'],
    }
    return jsonify(response),200

@app.route('/transactions/new', methods=['POST'])
def new_ransaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    index = blockchain.new_transaction_LMG(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain_LMG,
        'length': len(blockchain.chain_LMG)
    }
    return jsonify(response), 200

if __name__ == '__main__':
    print("Starting server...")
    app.run(host='0.0.0.0', port=5000)

