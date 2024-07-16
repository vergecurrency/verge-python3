```
____   _________________________   ________ ___________
\   \ /   /\_   _____/\______   \ /  _____/ \_   _____/
 \   Y   /  |    __)_  |       _//   \  ___  |    __)_ 
  \     /   |        \ |    |   \\    \_\  \ |        \ 2024 VERGE
   \___/   /_______  / |____|_  / \______  //_______  /
                   \/         \/         \/         \/ 
```
<p align="left">
  <a href="https://github.com/vergecurrency/verge-python3/actions/workflows/python-app.yml">
  <img src="https://github.com/vergecurrency/verge-python3/actions/workflows/python-app.yml/badge.svg">
  </a>
</p>


# A Python3 library for the VERGE Client
This is a set of Python libraries that allows easy access to the
VERGE peer-to-peer cryptocurrency client API.

(note: for python 2.7 support, please see https://github.com/vergecurrency/verge-python)


Installation instructions
===========================

verge-python3 uses setuptools for the install script. There are no dependencies apart from Python3 itself.

```
  $ python3 setup.py build
  $ python3 setup.py install
```  

Connection to verge-qt
=========================
```
If you want to connect to verge-qt, add server=1 in your VERGE.conf:

 rpcuser=vergerpcuser
 rpcpassword=randompassword
 server=1
```

TODO
======

```
These things still have to be added:

- SSL support (including certificate verification) for managing remote verge daemons.

verge-python3 is a fork of bitcoin-python, which was originally created by the very 
talented and widely loved, Wladimir van der Laan. 
```
