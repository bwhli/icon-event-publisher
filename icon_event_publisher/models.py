import json
from pydantic import BaseModel, validator
from typing import Optional


class Log(BaseModel):
    type: str
    log_index: int
    max_log_index: int
    transaction_hash: str
    transaction_index: int
    address: str
    data: str
    indexed: str
    block_number: int
    block_timestamp: int
    block_hash: str
    item_id: str
    item_timestamp: Optional[str]
    method: str

    @validator("indexed")
    @classmethod
    def validate_indexed(cls, data):
        return cls._convert_hex_to_int(data)

    @validator("data")
    @classmethod
    def validate_data(cls, data):
        return cls._convert_hex_to_int(data)

    @staticmethod
    def _convert_hex_to_int(data):
        data = json.loads(data)
        formatted_data = []
        for element in data:
            if element[:2] == "0x" and element != "0x":
                formatted_data.append(int(element, 16))
            else:
                formatted_data.append(element)
        return formatted_data


class Tx(BaseModel):
    from_address: str
    to_address: str
    value: str
    block_timestamp: int
    hash: str
    block_number: int
    transaction_fee: str
    receipt_status: int
    type: str
    method: str
    data: str

    @validator("data")
    @classmethod
    def validate_indexed(cls, data):
        return json.loads(data)
