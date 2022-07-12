from functools import lru_cache

BALANCED_CONTRACTS = [
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
]

CRAFT_CONTRACTS = [
    "cx9c4698411c6d9a780f605685153431dcda04609f",  # Craft
    "cx2e6d0fc0eca04965d06038c8406093337f085fcf",  # CraftMultiToken
]


@lru_cache(maxsize=1)
def get_contracts():
    return BALANCED_CONTRACTS + CRAFT_CONTRACTS
