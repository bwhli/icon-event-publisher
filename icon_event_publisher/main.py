import os
from concurrent.futures import ThreadPoolExecutor
from time import sleep

import requests
from dotenv import load_dotenv
from rich import print

from icon_event_publisher.contracts import get_contracts
from icon_event_publisher.icx import Icx
from icon_event_publisher.models import Tx
from icon_event_publisher.processors import process_transaction
from icon_event_publisher.utils import is_production

load_dotenv()

CONTRACTS = get_contracts()


def main():

    # Initialize start block.
    if is_production() is True:
        latest_block = Icx.get_latest_block()
    else:
        latest_block = os.getenv("DEBUG_BLOCK")

    print(f"Initializing with Block {latest_block}...")

    while True:
        try:
            while True:
                url = f"https://tracker.icon.community/api/v1/transactions/block-number/{latest_block}?limit=100"
                r = requests.get(url)
                r.raise_for_status()
                transactions = r.json()
                if len(transactions) > 0:
                    valid_transactions = [
                        Tx(**tx)
                        for tx in transactions
                        if tx["status"] == "0x1" and tx["to_address"] in CONTRACTS
                    ]
                    if len(valid_transactions) > 0:
                        with ThreadPoolExecutor(
                            max_workers=len(valid_transactions)
                        ) as executor:
                            for tx in valid_transactions:
                                executor.submit(process_transaction, tx=tx)
                    break
                else:
                    sleep(1)
                    continue
        except Exception as e:
            print(e)
            continue
        else:
            if is_production() is False:
                return
            print(f"Processed Block {latest_block}")
            latest_block += 1
            continue


if __name__ == "__main__":
    main()
