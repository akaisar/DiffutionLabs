import os
import json

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

class Settings:
    INFURA_PROJECT_ID = os.environ.get("INFURA_PROJECT_ID")
    INFURA_WS_URL = f'wss://mainnet.infura.io/ws/v3/{os.environ.get("INFURA_PROJECT_ID")}'
    INFURA_HTTPS_URL = f'https://mainnet.infura.io/v3/{os.environ.get("INFURA_PROJECT_ID")}'
    WETH_USDC_UNISWAP_ADDRESS = os.environ.get('WETH_USDC_UNISWAP_ADDRESS')
    UNISWAP_WETH_USDC_ABI = ''

    def __init__(self):
        with open('abis/uniswap_weth_usdc_abi.json', 'r') as f:
            self.UNISWAP_WETH_USDC_ABI = json.load(f)

settings = Settings()
