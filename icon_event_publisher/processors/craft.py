from models import Tx
from rich import print
from utils import (
    comma_separator,
    format_token,
    hex_to_int,
    send_discord_notification,
)


def process_craft_transaction(tx: Tx, logs: list, log_methods: list):

    print("Processing Craft transaction...")

    message = None
    ext_url = None

    if tx.to_address == "cx9c4698411c6d9a780f605685153431dcda04609f":  # Craft
        if tx.method == "purchase":  # 38756541
            buyer_icx_address = tx.from_address
            price = tx.value
            id = tx.data["params"]["_id"]
            quantity = tx.data["params"]["_amount"]
            token_score = tx.data["params"]["_tokenScore"]
            message = ("👀", "testtest")

    if message is not None:
        return message, ext_url


def _get_craft_user_url(icx_address):
    return f"https://craft.network/user/{icx_address}"


def _get_nft_url(token_score, id):
    return f"https://craft.network/nft/{token_score}:{id}"
