import json
from web3 import Web3
from eth_account import Account

Account.enable_unaudited_hdwallet_features()

with open("../Wallet Checker/success.txt", "r") as f:
    mnemonics = f.read().strip().splitlines()

# Ethereum
eth_provider = Web3.HTTPProvider('https://mainnet.infura.io/v3/841f60ce9a1747338caa452efdd100ac')
web3_eth = Web3(eth_provider)

# Polygon (Matic)
matic_provider = Web3.HTTPProvider('https://white-floral-vineyard.matic.discover.quiknode.pro/500a06232520491e356168b0018d033989c1c283/')
web3_matic = Web3(matic_provider)

# Binance Smart Chain
bsc_provider = Web3.HTTPProvider('https://hidden-methodical-feather.bsc.discover.quiknode.pro/8efe10ab0de37ef55a9b81e411f47d94b809cc2e/')
web3_bsc = Web3(bsc_provider)

# Solana
sol_provider = Web3.HTTPProvider('https://warmhearted-solemn-feather.solana-mainnet.discover.quiknode.pro/67c23b7da9514046f5f230350e0c14d378affe02/')
web3_sol = Web3(sol_provider)

balances = []

for i, mnemonic in enumerate(mnemonics):
    try:
        # print("Correct address")
        account = Account.from_mnemonic(mnemonic)
        address = account.address
        eth_balance = web3_eth.eth.get_balance(address)
        matic_balance = web3_matic.eth.get_balance(address)
        bsc_balance = web3_bsc.eth.get_balance(address)
        # sol_balance = web3_sol.eth.get_balance(address)
        if eth_balance > 0 or matic_balance > 0 or bsc_balance > 0:
            balances.append({
                "address": address,
                "balances": {
                    "Ethereum": str(eth_balance),
                    "Polygon (Matic)": str(matic_balance),
                    "Binance Smart Chain": str(bsc_balance),
                    # "Solana": str(sol_balance),
                }
            })
    except:
        continue

with open("../Wallet Checker/balances.txt", "w") as f:
    json.dump(balances, f, indent=4)
