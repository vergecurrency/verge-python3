*******
Testing
*******

The easiest way to run the tests is to use::

    $ python tests/test.py

This will read the `~/.VERGE/VERGE.conf` configuration file and connect to
the local `VERGEd` instance.

The `--config` option can be used to read a different local configuration file,
you probably want to use the `--nolocal` option as well. This is useful if you
want to use a separate verge data directory for development purposes.

Configuration from environment variables
****************************************

This works independently from the previous methods. The recommended way to use
this is to install the
`bitcoin testnet box <https://github.com/freewil/bitcoin-testnet-box>`_.
After a `make start` inside the box you should be able to run the tests with::

	HOST=localhost USER1=admin1 PORT1=20102 USER2=admin2 PORT2=21102 PASS=123 python tests/test.py --envconfig

This was primarily added to make continuous integration with
`travis-ci <http://about.travis-ci.org/>`_ possible. The environment variables
in the `.travis.yml` file are encrypted as described in
http://about.travis-ci.org/docs/user/build-configuration/#Secure-environment-variables
and use a testnetbox outside of travis to avoid installing the testnet box all
the time.