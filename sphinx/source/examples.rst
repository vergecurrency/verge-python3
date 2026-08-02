****************************
  Examples
****************************

A basic program that uses ``python-verge`` looks like this:

First, import the library.

::

    import vergerpc

Then, we connect to the currently running ``verge`` instance of the current user on the local machine
with one call to
:func:`~vergerpc.connect_to_local`. This returns a :class:`~vergerpc.connection.VERGEConnection` objects:

::

    conn = vergerpc.connect_to_local()

Retrieve modern server information and SMSG status:

::  

    chain = conn.getblockchaininfo()
    network = conn.getnetworkinfo()
    print("Blocks:", chain["blocks"])
    print("Connections:", network["connections"])
    print("SMSG:", conn.smsginfo())
  

