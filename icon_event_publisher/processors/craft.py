from models import Tx
from rich import print
from utils import (
    comma_separator,
    format_token,
    get_tracker_url,
    hex_to_int,
    send_discord_notification,
    shorten_icx_address
)


def process_craft_transaction(tx: Tx, logs: list, log_methods: list):

    # Utility functions related to Craft.
    def _get_craft_user_url(icx_address):
        return f"https://craft.network/user/{icx_address}"

    def _get_nft_url(token_score, id):
        return f"https://craft.network/nft/{token_score}:{id}"

    print("Processing Craft transaction...")

    message = None

    if tx.to_address == "cx9c4698411c6d9a780f605685153431dcda04609f":  # Craft
        if tx.method == "purchase":  # 38756541
            price = hex_to_int(tx.value)
            id = tx.data["params"]["_id"]
            quantity = tx.data["params"]["_amount"]
            token_score = tx.data["params"]["_tokenScore"]
            message = f"🛒 [{shorten_icx_address(tx.from_address)}]({_get_craft_user_url(tx.from_address)}) purchased {quantity} unit of [#{id}]({_get_nft_url(token_score, id)}) for {format_token(price, 'ICX')} [➡️](<{get_tracker_url(tx.hash)}>)"
        if tx.method == "makeOffer":
            price = hex_to_int(tx.value)
            id = tx.data["params"]["_id"]
            quantity = tx.data["params"]["_amount"]
            token_score = tx.data["params"]["_tokenScore"]
            message = f"🙋‍♂️ [{shorten_icx_address(tx.from_address)}]({_get_craft_user_url(tx.from_address)}) made a {format_token(price, 'ICX')} offer for {quantity} unit of [#{id}]({_get_nft_url(token_score, id)}) [➡️](<{get_tracker_url(tx.hash)}>)"
        if tx.method == "acceptOffer": # 38734953
            print(tx.value)

    return message


