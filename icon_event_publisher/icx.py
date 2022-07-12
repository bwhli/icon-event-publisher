import os

import requests
from dotenv import load_dotenv
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider

from models import Log

load_dotenv()


class Icx:

    ICON_SERVICE = IconService(HTTPProvider(os.environ["CTZ_API_ENDPOINT"], 3))

    def __init__(self) -> None:
        pass

    @classmethod
    def get_event_logs(cls, tx_hash: str):
        try:
            url = (
                f"https://tracker.icon.community/api/v1/logs?transaction_hash={tx_hash}"
            )
            r = requests.get(url)
            if r.status_code == 200:
                raw_logs = r.json()
                logs = [Log(**log) for log in raw_logs]
                return logs
            else:
                return None
        except Exception as e:
            print(e)
            print(tx_hash)

    @classmethod
    def get_from_address(cls, tx_hash: str):
        try:
            result = cls.ICON_SERVICE.get_transaction(tx_hash)["from"]
            return result
        except Exception as e:
            print(e)
            print(tx_hash)

    @classmethod
    def get_latest_block(cls):
        try:
            result = cls.ICON_SERVICE.get_block("latest")["height"]
            return result
        except Exception as e:
            print(e)

    @classmethod
    def get_transaction_info(cls, tx_hash: str):
        try:
            result = cls.ICON_SERVICE.get_transaction(tx_hash)
            return result
        except Exception as e:
            print(e)
            print(tx_hash)
