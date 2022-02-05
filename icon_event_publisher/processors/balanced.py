import ast
from models import Tx
from rich import print
from utils import comma_separator, format_token, get_tracker_url, hex_to_int, shorten_icx_address


def process_balanced_transaction(tx: Tx, logs: list, log_methods: list):

    print("Processing Balanced transaction...")

    message = None
    ext_url = None

    if "Swap" in log_methods:  # Balanced Swaps
        swap_logs = [log for log in logs if log.method in ("Swap", "ICXTransfer")]
        if len(swap_logs) == 1:  # 45586790 (bnUSD -> sICX)
            swap_log = swap_logs[0]
            from_token = swap_log.data[0]
            from_value = swap_log.data[4]
            to_token = swap_log.data[1]
            to_value = swap_log.data[5]
        else:  # bnUSD -> BALN -> sICX -> bnUSD
            _from = swap_logs[0]  # First swap log.
            _to = swap_logs[-1]  # Last swap log.
            if _from.method == "ICXTransfer":  # Swap from ICX.
                from_token = None
                from_value = _from.indexed[3]
                to_token = _to.data[1]
                to_value = _to.data[5]
                print(from_token, from_value, to_token, to_value)
            elif _to.method == "ICXTransfer":  # Swap to ICX.
                from_token = _from.data[0]
                from_value = _from.data[4]
                to_token = None
                to_value = _to.indexed[3]
            else:  # Other multi-hop swaps.
                from_token = _from.data[0]
                from_value = _from.data[4]
                to_token = _to.data[1]
                to_value = _to.data[5]
        message = (
            "🔄",
            f"swapped {format_token(from_value, from_token)} for {format_token(to_value, to_token)}",
        )

    if tx.to_address == "cxa0af3165c08318e988cb30993b3048335b94af6c":  # Balanced DEX
        if tx.method == "add":  # 45581661
            base_token = tx.data["params"]["_baseToken"]
            base_amount = int(tx.data["params"]["_baseValue"], 16)
            quote_token = tx.data["params"]["_quoteToken"]
            quote_amount = int(tx.data["params"]["_quoteValue"], 16)
            message = (
                "💧",
                f"supplied {format_token(base_amount, base_token)} and {format_token(quote_amount, quote_token)}",
            )

    if tx.to_address == "cx203d9cd2a669be67177e997b8948ce2c35caffae":  # Balanced Dividends
        if tx.method == "claim":  # 45588380
            log = [log for log in logs if log.method == "Claimed"][0]
            dividends = ast.literal_eval(log.data[2])
            nonzero_dividends = [
                f"{format_token(amount, contract)}" for contract, amount in dividends.items() if amount > 0
            ]
            if len(nonzero_dividends) > 0:
                message = (
                    "🤑",
                    f"claimed {comma_separator(nonzero_dividends)}",
                )

    if tx.method == "remove":  # 45583297
        logs = [log for log in logs if log.method in ("Withdraw")]
        base_token = logs[0].indexed[1]
        base_amount = logs[0].data[0]
        quote_token = logs[1].indexed[1]
        quote_amount = logs[1].data[0]
        message = (
            "💧",
            f"withdrew {format_token(base_amount, base_token)} and {format_token(quote_amount, quote_token)}",
        )

    if tx.to_address == "cx44250a12074799e26fdeee75648ae47e2cc84219":  # Balanced Governance
        if tx.method == "castVote":  # 45561816
            log = [log for log in logs if log.method == "VoteCast"][0]
            vote_index = hex_to_int(tx.data["params"]["vote_index"])
            vote_weight = log.data[1]
            if log.indexed[2] == 1:
                vote_side = "approved"
                emoji = "👍"
            else:
                vote_side = "rejected"
                emoji = "👎"
            message = (
                emoji,
                f"{vote_side} Proposal #{vote_index} with {format_token(vote_weight, 'BALN')}",
            )
            ext_url = f"https://app.balanced.network/vote/proposal/{vote_index}"

    if tx.to_address == "cx66d4d90f5f113eba575bf793570135f9b10cece1":  # Balanced Loans
        if tx.method == "depositAndBorrow":
            if "CollateralReceived" in log_methods:  # 45589689
                log = [log for log in logs if log.method == "CollateralReceived"][0]
                collateral_amount = log.data[0]
                collateral_token = log.indexed[2]
                message = ("🏦", f"deposited {format_token(collateral_amount, collateral_token)} as collateral")
            if "OriginateLoan" in log_methods:  # 45589694
                log = [log for log in logs if log.method == "OriginateLoan"][0]
                loan_amount = log.indexed[3]
                loan_token = log.indexed[2]
                message = ("🏦", f"minted {format_token(loan_amount, loan_token)}")

    if tx.to_address == "cx10d59e8103ab44635190bd4139dbfd682fa2d07e":  # Balanced Rewards
        if tx.method == "claimRewards":  # 45584850
            log = [log for log in logs if log.method == "RewardsClaimed"][0]
            claim_amount = log.data[0]
            message = ("🤑", f"claimed {format_token(claim_amount, 'BALN')}")

    if tx.to_address == "cxcfe9d1f83fa871e903008471cca786662437e58d":  # Balanced Worker Token
        total_distributions = sum([log.indexed[3] for log in logs])
        message = ("💸", f"Balanced distributed {format_token(total_distributions, 'BALN')} to BALW holders")

    ############
    ## TOKENS ##
    ############

    if tx.to_address == "cxf61cd5a45dc9f91c15aa65831a30a90d59a09619":  # BALN
        if tx.method == "stake":  # 45589689
            stake_amount = hex_to_int(tx.data["params"]["_value"])
            message = ("🥩", f"adjusted BALN stake to {format_token(stake_amount, 'BALN')}")

    # Format Discord notification message.
    if ext_url is None:
        ext_url = get_tracker_url(tx.hash)
    emoji, body = message[0], message[1]
    formatted_message = f"{emoji} `{shorten_icx_address(tx.from_address)}` [**{body}**](<{ext_url}>)"
    return formatted_message
