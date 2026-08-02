```
____   _________________________   ________ ___________
\   \ /   /\_   _____/\______   \ /  _____/ \_   _____/
 \   Y   /  |    __)_  |       _//   \  ___  |    __)_
  \     /   |        \ |    |   \\    \_\  \ |        \ 2026 VERGE
   \___/   /_______  / |____|_  / \______  //_______  /
                   \/         \/         \/     $XVG\/
```

[![Python](https://github.com/vergecurrency/verge-python3/actions/workflows/python-app.yml/badge.svg)](https://github.com/vergecurrency/verge-python3/actions/workflows/python-app.yml)

# Verge Core Python 3 binding

`verge-python3` is a Python JSON-RPC client for
[Verge Core v26.7](https://github.com/vergecurrency/verge/releases/tag/v26.7).
It includes the complete v26.7 Secure Messaging (SMSG) RPC surface. Deprecated
account APIs, `getinfo`, `signrawtransaction`, and obsolete mining RPCs are
intentionally not exposed.

## Requirements

- Python 3.10 or newer
- A running Verge Core v26.7 wallet or daemon with JSON-RPC enabled
- Python 3.14 for the same runtime used by the integration workflow

CI tests Python 3.10 through 3.14 and runs the binding against the official
v26.7 `verged` Ubuntu AppImage.

## Installation

From a checkout of this repository:

```console
python -m pip install .
```

For development and testing:

```console
python -m pip install -e ".[test]"
```

## Configure Verge Core

Add RPC credentials to `VERGE.conf`. Verge Qt also requires `server=1`:

```ini
server=1
rpcuser=vergerpcuser
rpcpassword=replace-with-a-long-random-password
```

Do not expose the RPC port to untrusted networks. `verged` disables SMSG by
default; start it with `-smsg=1` or add the following when SMSG access is
required:

```ini
smsg=1
```

Restart Verge Core after changing its configuration.

## Connect and call RPC methods

Connect using explicit credentials:

```python
import vergerpc

rpc = vergerpc.connect_to_remote(
    user="vergerpcuser",
    password="replace-with-a-long-random-password",
    host="127.0.0.1",
    port=20102,
)

chain = rpc.getblockchaininfo()
network = rpc.getnetworkinfo()

print("Chain:", chain["chain"])
print("Blocks:", chain["blocks"])
print("Connections:", network["connections"])
```

For a local Verge Core instance, the binding can read the standard
`VERGE.conf` location:

```python
import vergerpc

rpc = vergerpc.connect_to_local()
print(rpc.getwalletinfo())
```

Pass a configuration path when the file is in a nonstandard location:

```python
rpc = vergerpc.connect_to_local("/path/to/VERGE.conf")
```

## Labels and addresses

The deprecated account API has been replaced by labels:

```python
address = rpc.getnewaddress("customer-42")
rpc.setlabel(address, "customer-42")

print(rpc.getaddressesbylabel("customer-42"))
print(rpc.getreceivedbyaddress(address, minconf=1))
```

## Secure Messaging

With SMSG enabled:

```python
status = rpc.smsginfo()
address = rpc.getnewaddress("messages")

rpc.smsgaddlocaladdress(address)
chatkey = rpc.smsggetpubkey(address)

print(status)
print(chatkey["chatkey"])
```

Import a recipient's shared chatkey, then send a paid message:

```python
shared_chatkey = "RECIPIENT_ADDRESS-RECIPIENT_PUBLIC_KEY"
recipient_address, recipient_pubkey = shared_chatkey.split("-", 1)
rpc.smsgaddaddress(recipient_address, recipient_pubkey)

result = rpc.smsgsend(
    address_from=address,
    address_to=recipient_address,
    message="Hello from Python",
    paid_msg=True,
    days_retention=7,
)
print(result)
```

The wallet must contain enough confirmed XVG to fund a paid message.

## Testing

Run the local unit suite:

```console
python -m pytest
```

The GitHub Actions integration job downloads the official v26.7 Ubuntu
AppImages, starts `verged` on regtest with SMSG enabled, confirms that every
exposed binding method exists in daemon help, and exercises blockchain, wallet,
address, label, and SMSG calls. Pytest output capture is disabled for this job,
so RPC responses are visible in its Actions log.

To test an existing v26.7 daemon, set the integration environment variables
and run the daemon test:

```bash
VERGE_INTEGRATION=1 \
VERGE_RPC_USER=vergerpcuser \
VERGE_RPC_PASSWORD=replace-with-a-long-random-password \
VERGE_RPC_PORT=20102 \
python -m pytest tests/test_verged_v26_7.py -v -s
```

PowerShell:

```powershell
$env:VERGE_INTEGRATION = "1"
$env:VERGE_RPC_USER = "vergerpcuser"
$env:VERGE_RPC_PASSWORD = "replace-with-a-long-random-password"
$env:VERGE_RPC_PORT = "20102"
python -m pytest tests/test_verged_v26_7.py -v -s
```

The integration test requires a regtest daemon with SMSG enabled and must never
be pointed at a production wallet.

## Project history

`verge-python3` is derived from `bitcoin-python`, originally created by
Wladimir van der Laan.
