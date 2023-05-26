# The code uses API providers from different networks to check the balance of wallets
# whose mnemonic phrases have been determined to be valid. The results are written to a separate file.

from tqdm import tqdm
from web3 import Web3
from eth_account import Account

# Enable unaudited HD wallet features
Account.enable_unaudited_hdwallet_features()

# Read private keys from the file
with open("Correct_phrases.txt", "r") as f:
    private_keys = f.read().strip().splitlines()

# Define Ethereum and other network providers
eth_provider = Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_API_KEY')
arb_provider = Web3.HTTPProvider('https://arbitrum-mainnet.infura.io/v3/YOUR_API_KEY')
polygon_provider = Web3.HTTPProvider('https://polygon-mainnet.infura.io/v3/YOUR_API_KEY')
optimism_provider = Web3.HTTPProvider("https://optimism-mainnet.infura.io/v3/YOUR_API_KEY")

# Create web3 instances for each network
web3_eth = Web3(eth_provider)
web3_arb = Web3(arb_provider)
web3_polygon = Web3(polygon_provider)
web3_optimism = Web3(optimism_provider)

# Dictionary to store balances
balances = {}

# Initialize progress bar
progress_bar = tqdm(total=len(private_keys), unit="word(s)")

# Iterate over private keys
for i, private_key in enumerate(private_keys):
    # Get address from private key
    address = Account.from_mnemonic(private_key).address

    # Binance Smart Chain provider
    bsc_provider = Web3.HTTPProvider(
        f"https://api.bscscan.com/api?module=account&action=balance&address={address}&tag=latest&apikey=YOUR_API_KEY")
    web3_bsc = Web3(bsc_provider)

    # Check balances for each network
    eth_balance = web3_eth.eth.get_balance(address)
    if eth_balance > 0:
        balances.setdefault(address, {}).update({"Ethereum": str(eth_balance)})

    arb_balance = web3_arb.eth.get_balance(address)
    if arb_balance > 0:
        balances.setdefault(address, {}).update({"Arbitrum": str(arb_balance)})

    polygon_balance = web3_polygon.eth.get_balance(address)
    if polygon_balance > 0:
        balances.setdefault(address, {}).update({"Polygon": str(polygon_balance)})

    optimism_balance = web3_optimism.eth.get_balance(address)
    if optimism_balance > 0:
        balances.setdefault(address, {}).update({"Optimism": str(optimism_balance)})

    bsc_balance = web3_bsc.eth.get_balance(address)
    if bsc_balance > 0:
        balances.setdefault(address, {}).update({"BSC": str(bsc_balance)})

    progress_bar.update(1)

progress_bar.close()

# Write balances to the file
with open("balances.txt", "w") as f:
    for address, network_balances in balances.items():
        f.write(f"Address: {address}\n")
        for network, balance in network_balances.items():
            f.write(f"{network} - {balance}\n")
        f.write("\n")
