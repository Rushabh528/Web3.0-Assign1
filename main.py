import os
import json
import time, hashlib

def validate_transaction(transaction):
    
    txid = transaction["vin"][0]["txid"]
    if not txid:
        return False

    prevout_value = transaction["vin"][0]["prevout"]["value"]

    vout_values = [vout["value"] for vout in transaction["vout"]]
    total_vout_value = sum(vout_values)

    if prevout_value <= total_vout_value:
        return False

    return True

def read_json(directory):
    valid_transactions = []
    invalid_transactions = []

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                transaction = json.load(file)
                if validate_transaction(transaction):
                    valid_transactions.append(transaction)
                else:
                    invalid_transactions.append(transaction)
        

    return valid_transactions, invalid_transactions





coinbase_transaction={
  "txid": "4a7b8a1f3f6b3a9b8a1f3f6b3a9b8a1f3f6b3a7b8a1f3f6b3a9b8a1f3f6b3a9b",
  "vin": [
    {
      "coinbase": "04ffff001d0104455468652054696d65732030332f4a616e2f32303233204368616e63656c6c6f72206f6e20626974636f696e2062756c6c",
      "sequence": 4294967295
    }
  ],
  "vout": [
    {
      "value": 5000000000,
      "scriptPubKey": "4104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac"
    }
  ]
}


def calc_merkle_hash(txids):

    if len(txids)==0:
        return ''
    if len(txids)==1:
        return txids[0]

    while len(txids) > 1:
        if len(txids) % 2 != 0:
            txids.append(txids[-1])
        
        new_txids = []
        for i in range(0, len(txids), 2):
            new_txids.append(hashlib.sha256((txids[i] + txids[i + 1]).encode()).hexdigest())
        txids = new_txids
    
    return txids[0]


def block_header():
    current_timestamp = int(time.time())
    return {
        "version": 1,
        "hashPrevBlock": "0000111100000000000000000000000000000000000000000000000000000000",
        "hashMerkleRoot":calc_merkle_hash(
        [coinbase_transaction["txid"]] + [tx["vin"][0]["txid"] for tx in valid_transactions]
    ),
        "time": current_timestamp,
        "difficulty_target": "0000ffff00000000000000000000000000000000000000000000000000000000",
        "nonce": 0,
        }


def mine_block(block_header,difficulty_target):
    target=int(difficulty_target,16)
    nonce=0

    while True:
        # block_header['nonce']=nonce
        concatenated_string=str(block_header['version'])+block_header['hashPrevBlock']+block_header['hashMerkleRoot']+str(block_header['time'])+block_header['difficulty_target']+str(nonce)
        block_hash=hashlib.sha256(concatenated_string.encode()).hexdigest()
        if int(block_hash,16)<target:
            block_header['nonce']=nonce
            return nonce,block_hash
        nonce+=1



mempool_directory = "mempool"
valid_transactions, invalid_transactions = read_json(mempool_directory)
header=block_header()
nonce,block_hash=mine_block(header,"0000ffff00000000000000000000000000000000000000000000000000000000")
print(f'Nonce={nonce}')
print(f'block_hash={block_hash}')

with open("output.txt","w")as o:

    o.write("Block Header:"+ "\n")
    

    o.write(json.dumps(header,indent=2) + "\n")
    o.write("\n")
    o.write("Serialized Coinbase Transaction:"+ "\n")
    
    o.write(json.dumps(coinbase_transaction,indent=2) + "\n")
    o.write("\n")
    o.write("Transaction IDs:\n")

    for tx in valid_transactions:
            o.write(tx["vin"][0]["txid"] + "\n")
