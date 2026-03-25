import hashlib
import json
from typing import Dict

from bhagavad_gita_api.config import settings

try:
    from web3 import Web3
except ImportError:  # pragma: no cover
    Web3 = None


LOG_CHAT_ABI = [
    {
        "inputs": [{"internalType": "bytes32", "name": "chatHash", "type": "bytes32"}],
        "name": "logChat",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    }
]


class BlockchainError(RuntimeError):
    pass


class BlockchainDisabledError(BlockchainError):
    pass


def compute_chat_hash(user_input: str, response_payload: Dict[str, str]) -> str:
    serialized_response = json.dumps(
        response_payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    payload = f"{user_input}{serialized_response}"

    if Web3 is not None:
        return Web3.to_hex(Web3.keccak(text=payload))

    return "0x" + hashlib.sha3_256(payload.encode("utf-8")).hexdigest()


def normalize_chat_hash(chat_hash: str) -> str:
    normalized = chat_hash.strip().lower()
    if not normalized.startswith("0x"):
        normalized = f"0x{normalized}"
    if len(normalized) != 66:
        raise ValueError("Hash must be a 32-byte hex string.")
    return normalized


def log_chat_hash(chat_hash: str) -> str:
    normalized_hash = normalize_chat_hash(chat_hash)
    _validate_blockchain_config()

    if Web3 is None:
        raise BlockchainDisabledError("web3 is not installed.")

    web3 = Web3(Web3.HTTPProvider(settings.BLOCKCHAIN_RPC_URL))
    if not web3.is_connected():
        raise BlockchainError("Could not connect to the configured EVM RPC endpoint.")

    account = web3.eth.account.from_key(settings.BLOCKCHAIN_PRIVATE_KEY)
    contract = web3.eth.contract(
        address=Web3.to_checksum_address(settings.BLOCKCHAIN_CONTRACT_ADDRESS),
        abi=LOG_CHAT_ABI,
    )

    transaction = contract.functions.logChat(
        web3.to_bytes(hexstr=normalized_hash)
    ).build_transaction(
        _build_transaction_params(web3, account.address)
    )

    signed_transaction = account.sign_transaction(transaction)
    raw_transaction = getattr(
        signed_transaction,
        "rawTransaction",
        getattr(signed_transaction, "raw_transaction", None),
    )
    if raw_transaction is None:
        raise BlockchainError("Could not serialize the signed blockchain transaction.")
    transaction_hash = web3.eth.send_raw_transaction(raw_transaction)
    return transaction_hash.hex()


def _validate_blockchain_config() -> None:
    required_values = (
        settings.BLOCKCHAIN_RPC_URL,
        settings.BLOCKCHAIN_PRIVATE_KEY,
        settings.BLOCKCHAIN_CONTRACT_ADDRESS,
    )
    if not all(required_values):
        raise BlockchainDisabledError(
            "Blockchain logging is disabled. Configure RPC URL, contract address, and private key."
        )


def _build_transaction_params(web3, address: str) -> Dict[str, object]:
    params = {
        "from": address,
        "nonce": web3.eth.get_transaction_count(address),
        "gas": settings.BLOCKCHAIN_GAS_LIMIT,
        "chainId": settings.BLOCKCHAIN_CHAIN_ID or web3.eth.chain_id,
    }

    latest_block = web3.eth.get_block("latest")
    if latest_block.get("baseFeePerGas") is not None:
        max_priority_fee = getattr(web3.eth, "max_priority_fee", None)
        if callable(max_priority_fee):
            max_priority_fee = max_priority_fee()
        if max_priority_fee is None:
            max_priority_fee = web3.to_wei(2, "gwei")
        params["maxPriorityFeePerGas"] = max_priority_fee
        params["maxFeePerGas"] = latest_block["baseFeePerGas"] * 2 + max_priority_fee
    else:
        params["gasPrice"] = web3.eth.gas_price

    return params
