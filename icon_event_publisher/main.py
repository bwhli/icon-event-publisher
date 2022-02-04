import os
import requests
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from icx import Icx
from models import Tx
from processors import process_transaction
from rich import print
from time import sleep
from utils import is_production

load_dotenv()


def main():

    # Initialize start block.
    if is_production() is True:
        latest_block = Icx().get_latest_block()
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
                        Tx(**tx) for tx in transactions if tx["receipt_status"] == 1 and tx["from_address"] != "None"
                    ]
                    if len(valid_transactions) > 0:
                        with ThreadPoolExecutor(max_workers=len(valid_transactions)) as executor:
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
