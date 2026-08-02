import inspect

from vergerpc.connection import VERGEConnection
from vergerpc.proxy import AuthServiceProxy, FakeTransport


DEPRECATED_OR_REMOVED = {
    "getaccount",
    "getaccountaddress",
    "getaddressesbyaccount",
    "getblocknumber",
    "getgenerate",
    "gethashespersec",
    "getreceivedbyaccount",
    "getwork",
    "listaccounts",
    "listreceivedbyaccount",
    "move",
    "sendfrom",
    "setaccount",
    "setgenerate",
    "signrawtransaction",
}

SMSG_COMMANDS = {
    "flushsmgsdb",
    "smsg",
    "smsgaddaddress",
    "smsgaddlocaladdress",
    "smsgbuckets",
    "smsgdisable",
    "smsgenable",
    "smsggetpubkey",
    "smsgimportprivkey",
    "smsginbox",
    "smsginfo",
    "smsglocalkeys",
    "smsgoptions",
    "smsgoutbox",
    "smsgpurge",
    "smsgscanbuckets",
    "smsgscanchain",
    "smsgsend",
    "smsgsendanon",
    "smsgview",
}


def public_methods():
    return {
        name
        for name, member in inspect.getmembers(VERGEConnection, inspect.isfunction)
        if not name.startswith("_")
    }


def test_deprecated_and_removed_rpc_wrappers_are_absent():
    assert DEPRECATED_OR_REMOVED.isdisjoint(public_methods())


def test_complete_v26_7_smsg_surface_is_exposed():
    assert SMSG_COMMANDS <= public_methods()


def test_smsgsend_forwards_v26_7_arguments():
    transport = FakeTransport()
    transport.load_raw("smsgsend", {"result": {"result": "Sent."}, "error": None, "id": 1})
    connection = VERGEConnection("user", "pass")
    connection.proxy = AuthServiceProxy(
        "http://user:pass@localhost:1", transport=transport
    )
    assert connection.smsgsend("from", "to", "hello", days_retention=7)["result"] == "Sent."
