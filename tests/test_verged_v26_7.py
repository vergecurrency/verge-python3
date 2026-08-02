import inspect
import json
import os

import pytest

from vergerpc import connect_to_remote
from vergerpc.connection import VERGEConnection


pytestmark = pytest.mark.skipif(
    os.getenv("VERGE_INTEGRATION") != "1",
    reason="set VERGE_INTEGRATION=1 to test a running Verge Core v26.7 daemon",
)


def connection():
    return connect_to_remote(
        user=os.environ["VERGE_RPC_USER"],
        password=os.environ["VERGE_RPC_PASSWORD"],
        host=os.getenv("VERGE_RPC_HOST", "127.0.0.1"),
        port=int(os.environ["VERGE_RPC_PORT"]),
    )


def show(method, result):
    print(f"\n{method}:")
    print(json.dumps(result, indent=2, default=str, sort_keys=True))
    return result


def rpc_methods():
    return {
        name
        for name, member in inspect.getmembers(VERGEConnection, inspect.isfunction)
        if not name.startswith("_")
    }


def test_all_wrapped_commands_exist_in_v26_7():
    rpc = connection()
    for method in sorted(rpc_methods()):
        help_text = rpc.proxy.help(method)
        assert help_text.lower().startswith(method), method
        print(f"help {method}: available")


def test_v26_7_daemon_and_smsg_smoke():
    rpc = connection()
    network = show("getnetworkinfo", rpc.getnetworkinfo())
    chain = show("getblockchaininfo", rpc.getblockchaininfo())
    wallet = show("getwalletinfo", rpc.getwalletinfo())
    smsg = show("smsginfo", rpc.smsginfo())

    assert network["version"] // 10_000 == 2607
    assert chain["chain"] == "regtest"
    assert "walletversion" in wallet
    assert smsg["enabled"] is True

    address = show("getnewaddress", rpc.getnewaddress("integration"))
    validation = rpc.validateaddress(address)
    show("validateaddress", validation.__dict__)
    assert validation.isvalid is True
    assert show("getaddressesbylabel", rpc.getaddressesbylabel("integration"))
    show("smsgaddlocaladdress", rpc.smsgaddlocaladdress(address))
    assert show("smsggetpubkey", rpc.smsggetpubkey(address))
