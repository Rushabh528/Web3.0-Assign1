So, I have divided the solution into three parts.I will be explaining each of those in the following sections:

1.Validating the transactions(validate_transaction):First of all , I validated the given transactions in the mempool folder and stored them in a list. I used a loop for satisfying the two conditions required to check if a given transaction is valid or not. Then I used a coinbase transaction(given in the sample output.txt file in the repo).

2.Creating the block(block_header): Then I created the block by involving the required key-vakue pairs, using the merkle hash of the txids concatenated(both the coinbase and each of the valid transactions).

3.Mining the block and writing the output: Then I passed the block_header and difficulty target in the mine_block function and mined the block when block hash is less than the difficulty target. Then I wrote the output (along with proper format)in the output.txt file.