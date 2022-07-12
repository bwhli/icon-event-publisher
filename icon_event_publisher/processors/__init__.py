import os

from contracts import BALANCED_CONTRACTS, CRAFT_CONTRACTS
from icx import Icx
from models import Tx
from processors.balanced import process_balanced_transaction
from processors.craft import process_craft_transaction
from rich import print
from utils import is_production, send_discord_notification


def process_transaction(tx: Tx):

    # Get event logs
    logs = Icx.get_event_logs(tx.hash)

    if logs is not None:
        log_methods = [log.method for log in logs]
    else:
        log_methods = []

    if tx.to_address in BALANCED_CONTRACTS or "Swap" in log_methods:
        print(f"{tx.hash}: Balanced")
        discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL_BALANCED")
        message = process_balanced_transaction(tx, logs, log_methods)

    if is_production is False:
        if tx.to_address in CRAFT_CONTRACTS:
            discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL_CRAFT")
            message = process_craft_transaction(tx, logs, log_methods)

    if is_production() is False:
        discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL_DEBUG")

    if message is not None:
        send_discord_notification(message, discord_webhook_url)
