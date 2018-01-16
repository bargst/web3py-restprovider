import pytest
from web3 import Web3
from web3_restprovider import RESTProvider


@pytest.fixture
def provider():
    return RESTProvider('https://api.infura.io/v1/jsonrpc/mainnet')


def test_connected_invalid():
    web3 = Web3(RESTProvider('http://doesnotexist:8080'))
    assert web3.isConnected() is False


def test_requests(provider):
    web3 = Web3(provider)
    assert web3.isConnected() is True
    assert web3.eth.getBlock(12345) == web3.eth.getBlock('0x767c2bfb3bdee3f78676c1285cd757bcd5d8c272cef2eb30d9733800a78c0b6d')
