from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
import time

from web3 import Web3
from websockets import connect
from web3.middleware import geth_poa_middleware

from settings import settings

class UniswapParser:
    def __init__(self):
        w3 = Web3(Web3.HTTPProvider(settings.INFURA_HTTPS_URL))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        Web3.to_checksum_address(settings.WETH_USDC_UNISWAP_ADDRESS)
        self.w3 = w3

        self.uniswap_contract = w3.eth.contract(address=settings.WETH_USDC_UNISWAP_ADDRESS, abi=settings.UNISWAP_WETH_USDC_ABI)

    def __get_swap_events(self, block_number):
        block = self.w3.eth.get_block(block_number)

        swap_events = []

        for tx in block.transactions:
            tx_receipt = self.w3.eth.get_transaction_receipt(tx.hex())
            for log in tx_receipt['logs']:
                if log['address'].lower() == settings.WETH_USDC_UNISWAP_ADDRESS.lower():
                    try:
                        swap_event = self.uniswap_contract.events.Swap().process_log(log)
                        swap_events.append(swap_event)
                    except:
                        continue
        return swap_events

    def __handle_swap_event(self, event):
        tx_hash = event['transactionHash'].hex()
        sender = event['args']['sender']
        amount1_in = event['args']['amount1In']
        amount0_in = event['args']['amount0In']
        amount0_out = event['args']['amount0Out']
        amount1_out = event['args']['amount1Out']
        timestamp = self.w3.eth.get_block(event['blockNumber'])['timestamp']

        print(f"Transaction Hash: {tx_hash}")
        print(f"Sender Address: {sender}")
        print(f"Amount of WETH Swapped to USDC: {self.w3.from_wei(amount1_in, 'ether')} WETH to {self.w3.from_wei(amount0_out, 'mwei')} USDC")
        print(f"Amount of USDC Swapped to WETH: {self.w3.from_wei(amount0_in, 'mwei')} USDC to {self.w3.from_wei(amount1_out, 'ether')} WETH")

        print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(timestamp))}\n")
    
    def print_swap_events_for_block(self, block_number):
        swap_events = self.__get_swap_events(block_number)
        for swap_event in swap_events:
            self.__handle_swap_event(swap_event)

uniswap_parser = UniswapParser()
