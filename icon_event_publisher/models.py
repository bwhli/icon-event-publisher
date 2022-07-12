from typing import Union

import rapidjson
from pydantic import BaseModel, validator

from icon_event_publisher.utils import convert_hex_to_int


class Log(BaseModel):

    address: str
    block_number: int
    block_timestamp: int
    data: Union[str, None]
    indexed: str
    log_index: int
    method: str
    transaction_hash: str

    @validator("indexed")
    @classmethod
    def validate_indexed(cls, data):
        if data is not None:
            return convert_hex_to_int(data)
        else:
            return None

    @validator("data")
    @classmethod
    def validate_data(cls, data):
        try:
            return convert_hex_to_int(data)
        except:
            return None


class Tx(BaseModel):
    block_number: int
    block_timestamp: int
    data: str
    from_address: str
    hash: str
    method: str
    status: str
    to_address: str
    type: str
    value: str
    value_decimal: int

    @validator("data")
    @classmethod
    def validate_indexed(cls, data):
        return rapidjson.loads(data)
