*******
Testing
*******

Run the unit suite with::

    python -m pip install -e ".[test]"
    python -m pytest

The GitHub Actions integration job downloads the official Verge Core v26.7
Ubuntu AppImage, starts ``verged`` on regtest with SMSG enabled, checks that
each exposed command exists in daemon help, and runs wallet and SMSG smoke
tests.

To run the integration test against an already-running v26.7 daemon, set
``VERGE_INTEGRATION=1`` plus ``VERGE_RPC_USER``, ``VERGE_RPC_PASSWORD``, and
``VERGE_RPC_PORT`` before running ``pytest tests/test_verged_v26_7.py``.
