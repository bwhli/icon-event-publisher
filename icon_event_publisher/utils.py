import codecs
import os
import requests
from functools import lru_cache

TOKENS = {
    "cxf61cd5a45dc9f91c15aa65831a30a90d59a09619": {"ticker": "BALN", "precision": 18},
    "cx88fd7df7ddff82f7cc735c871dc519838cb235bb": {"ticker": "bnUSD", "precision": 18},
    "cx2e6d0fc0eca04965d06038c8406093337f085fcf": {"ticker": "CFT", "precision": 18},
    "cx785d504f44b5d2c8dac04c5a1ecd75f18ee57d16": {"ticker": "FIN", "precision": 18},
    "cx6139a27c15f1653471ffba0b4b88dc15de7e3267": {"ticker": "GBET", "precision": 18},
    "cxe7c05b43b3832c04735e7f109409ebcb9c19e664": {"ticker": "IAM", "precision": 18},
    "cxae3034235540b924dfcc1b45836c293dcc82bfb7": {"ticker": "IUSDC", "precision": 6},
    "cx3a36ea1f6b9aa3d2dd9cb68e8987bcc3aabaaa88": {"ticker": "IUSDT", "precision": 6},
    "cx369a5f4ce4f4648dfc96ba0c8229be0693b4eca2": {"ticker": "METX", "precision": 18},
    "cx1a29259a59f463a67bb2ef84398b30ca56b5830a": {"ticker": "OMM", "precision": 18},
    "cx2609b924e33ef00b648a409245c7ea394c467824": {"ticker": "sICX", "precision": 18},
    "cxbb2871f468a3008f80b08fdde5b8b951583acf06": {"ticker": "USDS", "precision": 18},
}

IGNORED_CONTRACTS = ["cxaa99a164586883eed0322d62a31946dfa9491fa6"]  # [Optimus]


#################
## TOKEN STUFF ##
#################


def get_token_ticker(contract: str):
    if contract is None or contract == "None":
        return "ICX"
    else:
        return TOKENS[contract]["ticker"]

@lru_cache(maxsize=1)
def get_token_tickers():
    token_tickers = [ TOKENS[contract]["ticker"] for contract in TOKENS.keys()]
    return token_tickers

def get_token_precision(contract: str):
    if contract[:2] != "cx":
        contract = get_token_contract(contract)
    if contract is None or contract == "None":
        return 18
    else:
        return TOKENS[contract]["precision"]


def get_token_contract(ticker: str):
    for k, v in TOKENS.items():
        if v["ticker"] == ticker:
            return k


@lru_cache(maxsize=1)
def get_token_contracts():
    return list(TOKENS.keys())


#####################
## TEXT FORMATTING ##
#####################


def comma_separator(sequence):
    if len(sequence) > 1:
        return "{}, and {}".format(", ".join(sequence[:-1]), sequence[-1])


def decode_hex_string(input):
    if input[:2] == "0x":
        input = input[2:]
    result = codecs.decode(input, "hex").decode("utf-8")
    print(result)
    return result


def format_token(token_amount: int, token_contract: str):
    if token_contract == "ICX":
        token_precision = 18
        token_symbol = "ICX"
    else:
        if token_contract in get_token_tickers():
            token_contract = get_token_contract(token_contract)
        token_symbol = get_token_ticker(token_contract)
        token_precision = get_token_precision(token_contract)
    token_amount = token_amount / 10 ** token_precision
    if token_amount.is_integer() is True:
        result = f"{token_amount:,.{0}f} {token_symbol}"
    else:
        result = f"{token_amount:,.{4}f} {token_symbol}"
    return result

def get_tracker_url(tx_hash: str):
    return f"https://tracker.icon.community/transaction/{tx_hash}"

def hex_to_int(input):
    result = int(input, 16)
    return result

def shorten_icx_address(icx_address: str):
    return f"{icx_address[:4]}...{icx_address[-4:]}"


###################
## DISCORD STUFF ##
###################


def send_discord_notification(message: str, discord_webhook_url: str):
    print(message)
    payload = {
        "username": "Balanced Activity Monitor",
        "avatar_url": "https://brianli.com/balanced/balanced-dao.png",
        "content": message,
    }
    r = requests.post(discord_webhook_url, json=payload)
    if r.status_code == 204:
        print("Message Delivered!")
    else:
        print("Message Not Delivered!")


##########
## MISC ##
##########


@lru_cache(maxsize=1)
def is_production():
    environment = os.getenv("ENV")
    if environment == "PRODUCTION":
        return True
    else:
        return False
