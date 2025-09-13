import hashlib
import json

from time import time

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

        block = {
            'index': len(self.chain_LMG) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions_LMG,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain_LMG[-1]),
        }

        self.current_transactions_LMG = []
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
    def hash_LMG(block):
        """
        Creates SHA-256 block hash
        :param block: <dict> Block
        :return: <str> hashsum
        """

        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

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

blockchain = Blockchain()

print("Попередній блок...")
print(json.dumps(blockchain.last_block_LMG, indent=4))

print("\nМайнинг...")
last_block_proof = blockchain.last_block_LMG['proof']
new_proof = blockchain.proof_of_work_LMG(last_block_proof)

print(f"Хеш знайдено! PoW роботи: {new_proof}")

last_block_hash = blockchain.hash_LMG(blockchain.last_block_LMG)
new_block = blockchain.new_block_LMG(new_proof, last_block_hash)

print("Новий блок:")
print(json.dumps(new_block, indent=4))

print("\n" + "="*20)
print("ПЕРЕВІРКА РЕЗУЛЬТАТУ")
print("="*20)

guess_to_check = f'{last_block_proof}{new_proof}'.encode()
checked_hash = hashlib.sha256(guess_to_check).hexdigest()

print(f"Попередній PoW: {last_block_proof}")
print(f"Новий PoW: {new_proof}")
print(f"Хеш нового блоку: {checked_hash}")
print(f"Останні два символи хешу: '{checked_hash[-2:]}'")

month_to_check = "09"
if checked_hash.endswith(month_to_check):
    print(f"\n✅ Успіх! Хеш коректно закінчується на '{month_to_check}'.")
else:
    print(f"\n❌ Помилка Хеш не закінчується на '{month_to_check}'.")
