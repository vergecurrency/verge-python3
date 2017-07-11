![verge-python3](https://raw.githubusercontent.com/vergecurrency/verge-python3/master/verge-python3.png)
```
____   _________________________   ________ ___________
\   \ /   /\_   _____/\______   \ /  _____/ \_   _____/
 \   Y   /  |    __)_  |       _//   \  ___  |    __)_ 
  \     /   |        \ |    |   \\    \_\  \ |        \ 2017 VERGE
   \___/   /_______  / |____|_  / \______  //_______  /
                   \/         \/         \/         \/ 
```
# A Python3 library for the VERGE Client
This is a set of Python libraries that allows easy access to the
VERGE peer-to-peer cryptocurrency client API.

(note: for python 2.7 support, please see https://github.com/vergecurrency/verge-python)


Installation instructions
===========================

verge-python3 uses setuptools for the install script. There are no dependencies apart from Python3 itself.

::

  $ python setup.py build
  $ python setup.py install
  

Pypi / Cheeseshop (coming soon)
==================
```
It is possible to install the package through Pypi (cheeseshop), see http://pypi.python.org/pypi?:action=display&name=verge-python3
::
 $ pip install verge-python3
 # if not working, try
 $ pip install --pre verge-python3
```
Connection to verge-qt
=========================
```
If you want to connect to verge-qt, add server=1 in your VERGE.conf
::

 rpcuser=vergerpcuser
 rpcpassword=randompassword
 server=1
```
TODO
======

```
These things still have to be added:

- SSL support (including certificate verification) for managing remote verge daemons.

verge-python3 is a fork of bitcoin-python : https://github.com/laanwj/bitcoin-python
```