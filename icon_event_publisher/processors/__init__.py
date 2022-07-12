import os

from icx import Icx
from models import Tx
from rich import print
from utils import is_production, send_discord_notification

from processors.balanced import process_balanced_transaction
from processors.craft import process_craft_transaction

BALANCED_CONTRACTS = (
    "cxa0af3165c08318e988cb30993b3048335b94af6c",  # Balanced DEX
    "cx66d4d90f5f113eba575bf793570135f9b10cece1",  # Balanced Loans
    "cx203d9cd2a669be67177e997b8948ce2c35caffae",  # Balanced Dividends
    "cx44250a12074799e26fdeee75648ae47e2cc84219",  # Balanced Governance
    "cxf58b9a1898998a31be7f1d99276204a3333ac9b3",  # Balanced Reserve Fund
    "cx43e2eec79eb76293c298f2b17aec06097be606e0",  # Balanced Staking
    "cx835b300dcfe01f0bdb794e134a0c5628384f4367",  # Balanced DAO Fund
    "cx10d59e8103ab44635190bd4139dbfd682fa2d07e",  # Balanced Rewards
    "cx40d59439571299bca40362db2a7d8cae5b0b30b0",  # Balanced Rebalance
    "cx21e94c08c03daee80c25d8ee3ea22a20786ec231",  # Balanced Router
    "cxcfe9d1f83fa871e903008471cca786662437e58d",  # Balanced Worker Token
)

CRAFT_CONTRACTS = (
    "cx9c4698411c6d9a780f605685153431dcda04609f",  # Craft
    "cx2e6d0fc0eca04965d06038c8406093337f085fcf",  # CraftMultiToken
)


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

    #    if is_production is False:
    #        if tx.to_address in CRAFT_CONTRACTS:
    #            discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL_CRAFT")
    #            message = process_craft_transaction(tx, logs, log_methods)
    #
    #    if is_production() is False:
    #        discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL_DEBUG")

    if message is not None:
        send_discord_notification(message, discord_webhook_url)
