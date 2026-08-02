```
____   _________________________   ________ ___________
\   \ /   /\_   _____/\______   \ /  _____/ \_   _____/
 \   Y   /  |    __)_  |       _//   \  ___  |    __)_ 
  \     /   |        \ |    |   \\    \_\  \ |        \ 2024 VERGE
   \___/   /_______  / |____|_  / \______  //_______  /
                   \/         \/         \/     $XVG\/ 
```
<p align="left">
  <a href="https://github.com/vergecurrency/verge-python3/actions/workflows/python-app.yml">
  <img src="https://github.com/vergecurrency/verge-python3/actions/workflows/python-app.yml/badge.svg">
  </a>
</p>


# A Python 3 library for Verge Core

This package provides a friendly JSON-RPC binding for Verge Core v26.7,
including its complete Secure Messaging (SMSG) RPC surface. Deprecated account
RPCs and obsolete mining RPCs are intentionally not exposed.

(note: for python 2.7 support, please see https://github.com/vergecurrency/verge-python)


## Installation

Python 3.10 or newer is required. Python 3.14 is tested in CI.

```
python -m pip install .
```  

## Connection to verge-qt

If you want to connect to verge-qt, add server=1 in your VERGE.conf:

```
rpcuser=vergerpcuser
rpcpassword=randompassword
server=1
```

```python
import vergerpc

rpc = vergerpc.connect_to_remote(
    user="vergerpcuser",
    password="randompassword",
    port=20102,
)
print(rpc.getblockchaininfo())
print(rpc.smsginfo())
```

## Testing

Unit tests run with `python -m pytest`. The GitHub Actions integration job
downloads the official Verge Core v26.7 Ubuntu AppImage, starts `verged` on
regtest with SMSG enabled, verifies every exposed method through daemon help,
and performs blockchain, wallet, address, label, and SMSG smoke tests.

## TODO

```
These things still have to be added:

- SSL support (including certificate verification) for managing remote verge daemons.

verge-python3 is a fork of bitcoin-python, which was originally created by the very 
talented and widely loved, Wladimir van der Laan. 
```
