import json
from decimal import Decimal

import pytest

from vergerpc.config import read_config_file
from vergerpc.exceptions import InvalidParameter
from vergerpc.proxy import AuthServiceProxy, FakeTransport


def test_proxy_preserves_decimal_and_wraps_rpc_errors():
    transport = FakeTransport()
    transport.load_raw("getbalance", {"result": Decimal("1.25"), "error": None, "id": 1})
    proxy = AuthServiceProxy("http://user:pass@localhost:1", transport=transport)
    assert proxy.getbalance() == Decimal("1.25")

    transport.load_raw(
        "example",
        {"result": None, "error": {"code": -8, "message": "bad value"}, "id": 2},
    )
    wrapped = AuthServiceProxy(
        "http://user:pass@localhost:1",
        transport=transport,
        exception_wrapper=lambda error: InvalidParameter(error),
    )
    with pytest.raises(InvalidParameter):
        wrapped.example()


def test_config_parser_ignores_comments(tmp_path):
    config = tmp_path / "VERGE.conf"
    config.write_text("# comment\nrpcuser=user\n; ignored=1\nrpcpassword=secret\n", encoding="utf-8")
    assert read_config_file(config) == {"rpcuser": "user", "rpcpassword": "secret"}


def test_rpc_request_is_json_rpc_1_1_compatible():
    transport = FakeTransport()
    transport.load_raw("echo", {"result": "ok", "error": None, "id": 1})
    proxy = AuthServiceProxy("http://user:pass@localhost:1", transport=transport)
    assert proxy.echo("ok") == "ok"
