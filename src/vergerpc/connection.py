"""Typed convenience methods for the Verge Core v26.7 JSON-RPC API."""

from urllib.parse import quote

from vergerpc.data import AddressInfo, AddressValidation, MiningInfo, TransactionInfo
from vergerpc.exceptions import (
    VERGEException,
    WalletAlreadyUnlocked,
    WalletPassphraseIncorrect,
    wrap_exception,
)
from vergerpc.proxy import AuthServiceProxy


class VERGEConnection:
    """A connection to a Verge Core JSON-RPC server."""

    def __init__(self, user, password, host="localhost", port=20102, use_https=False):
        scheme = "https" if use_https else "http"
        self.url = "{}://{}:{}@{}:{}/".format(
            scheme, quote(user, safe=""), quote(password, safe=""), host, port
        )
        self.proxy = AuthServiceProxy(self.url, exception_wrapper=wrap_exception)

    # Control, network, blockchain, and mining
    def stop(self):
        return self.proxy.stop()

    def getblockchaininfo(self):
        return self.proxy.getblockchaininfo()

    def getnetworkinfo(self):
        return self.proxy.getnetworkinfo()

    def getwalletinfo(self):
        return self.proxy.getwalletinfo()

    def getblock(self, block_hash, verbosity=1):
        return self.proxy.getblock(block_hash, verbosity)

    def getblockcount(self):
        return self.proxy.getblockcount()

    def getblockhash(self, height):
        return self.proxy.getblockhash(height)

    def getbestblockhash(self):
        return self.proxy.getbestblockhash()

    def getconnectioncount(self):
        return self.proxy.getconnectioncount()

    def getdifficulty(self):
        return self.proxy.getdifficulty()

    def getmininginfo(self):
        return MiningInfo(**self.proxy.getmininginfo())

    def generatetoaddress(self, nblocks, address, maxtries=1_000_000):
        return self.proxy.generatetoaddress(nblocks, address, maxtries)

    # Wallet and labels
    def getnewaddress(self, label="", address_type=None):
        if address_type is None:
            return self.proxy.getnewaddress(label)
        return self.proxy.getnewaddress(label, address_type)

    def getaddressinfo(self, address):
        return self.proxy.getaddressinfo(address)

    def setlabel(self, address, label):
        return self.proxy.setlabel(address, label)

    def getaddressesbylabel(self, label):
        return self.proxy.getaddressesbylabel(label)

    def listlabels(self, purpose=None):
        return self.proxy.listlabels() if purpose is None else self.proxy.listlabels(purpose)

    def getreceivedbyaddress(self, address, minconf=1):
        return self.proxy.getreceivedbyaddress(address, minconf)

    def getreceivedbylabel(self, label, minconf=1):
        return self.proxy.getreceivedbylabel(label, minconf)

    def listreceivedbyaddress(
        self, minconf=1, include_empty=False, include_watchonly=False, address_filter=None
    ):
        args = [minconf, include_empty, include_watchonly]
        if address_filter is not None:
            args.append(address_filter)
        return [AddressInfo(**item) for item in self.proxy.listreceivedbyaddress(*args)]

    def listreceivedbylabel(self, minconf=1, include_empty=False, include_watchonly=False):
        return self.proxy.listreceivedbylabel(minconf, include_empty, include_watchonly)

    def getbalance(self, minconf=0, include_watchonly=False):
        return self.proxy.getbalance("*", minconf, include_watchonly)

    def sendtoaddress(
        self,
        address,
        amount,
        comment="",
        comment_to="",
        subtract_fee_from_amount=False,
        replaceable=False,
        conf_target=None,
        estimate_mode=None,
    ):
        args = [address, amount, comment, comment_to, subtract_fee_from_amount, replaceable]
        if conf_target is not None:
            args.append(conf_target)
            if estimate_mode is not None:
                args.append(estimate_mode)
        return self.proxy.sendtoaddress(*args)

    def sendmany(
        self,
        amounts,
        minconf=1,
        comment="",
        subtract_fee_from=(),
        replaceable=False,
        conf_target=None,
        estimate_mode=None,
    ):
        args = ["", amounts, minconf, comment, list(subtract_fee_from), replaceable]
        if conf_target is not None:
            args.append(conf_target)
            if estimate_mode is not None:
                args.append(estimate_mode)
        return self.proxy.sendmany(*args)

    def listtransactions(self, count=10, skip=0, include_watchonly=False):
        return [
            TransactionInfo(**item)
            for item in self.proxy.listtransactions("*", count, skip, include_watchonly)
        ]

    def listsinceblock(
        self, block_hash=None, target_confirmations=1, include_watchonly=False, include_removed=True
    ):
        args = []
        if block_hash is not None:
            args = [block_hash, target_confirmations, include_watchonly, include_removed]
        result = self.proxy.listsinceblock(*args)
        result["transactions"] = [TransactionInfo(**item) for item in result["transactions"]]
        return result

    def gettransaction(self, txid, include_watchonly=False):
        return TransactionInfo(**self.proxy.gettransaction(txid, include_watchonly))

    def backupwallet(self, destination):
        return self.proxy.backupwallet(destination)

    def validateaddress(self, address):
        return AddressValidation(**self.proxy.validateaddress(address))

    def listunspent(
        self, minconf=1, maxconf=9_999_999, addresses=None, include_unsafe=True, query_options=None
    ):
        args = [minconf, maxconf]
        if addresses is not None:
            args.extend([addresses, include_unsafe])
            if query_options is not None:
                args.append(query_options)
        return [TransactionInfo(**item) for item in self.proxy.listunspent(*args)]

    def keypoolrefill(self, newsize=None):
        return self.proxy.keypoolrefill() if newsize is None else self.proxy.keypoolrefill(newsize)

    def importprivkey(self, privkey, label="", rescan=True):
        return self.proxy.importprivkey(privkey, label, rescan)

    def dumpprivkey(self, address):
        return self.proxy.dumpprivkey(address)

    def signmessage(self, address, message):
        return self.proxy.signmessage(address, message)

    def verifymessage(self, address, signature, message):
        return self.proxy.verifymessage(address, signature, message)

    def walletpassphrase(self, passphrase, timeout, dont_raise=False):
        try:
            self.proxy.walletpassphrase(passphrase, timeout)
            return True
        except VERGEException as exception:
            if dont_raise and isinstance(exception, WalletPassphraseIncorrect):
                return False
            if dont_raise and isinstance(exception, WalletAlreadyUnlocked):
                return True
            raise

    def walletlock(self):
        return self.proxy.walletlock()

    def walletpassphrasechange(self, oldpassphrase, newpassphrase, dont_raise=False):
        try:
            self.proxy.walletpassphrasechange(oldpassphrase, newpassphrase)
            return True
        except VERGEException as exception:
            if dont_raise and isinstance(exception, WalletPassphraseIncorrect):
                return False
            raise

    # Raw transactions
    def getrawtransaction(self, txid, verbose=True, block_hash=None):
        args = [txid, verbose]
        if block_hash is not None:
            args.append(block_hash)
        result = self.proxy.getrawtransaction(*args)
        return TransactionInfo(**result) if verbose else result

    def gettxout(self, txid, index, include_mempool=True):
        result = self.proxy.gettxout(txid, index, include_mempool)
        return None if result is None else TransactionInfo(**result)

    def createrawtransaction(self, inputs, outputs, locktime=0, replaceable=False):
        return self.proxy.createrawtransaction(inputs, outputs, locktime, replaceable)

    def decoderawtransaction(self, hexstring, iswitness=None):
        if iswitness is None:
            return self.proxy.decoderawtransaction(hexstring)
        return self.proxy.decoderawtransaction(hexstring, iswitness)

    def sendrawtransaction(self, hexstring, allowhighfees=False):
        return self.proxy.sendrawtransaction(hexstring, allowhighfees)

    def signrawtransactionwithwallet(self, hexstring, previous_transactions=None, sighashtype=None):
        args = [hexstring]
        if previous_transactions is not None or sighashtype is not None:
            args.append(previous_transactions or [])
            if sighashtype is not None:
                args.append(sighashtype)
        return self.proxy.signrawtransactionwithwallet(*args)

    def signrawtransactionwithkey(
        self, hexstring, private_keys, previous_transactions=None, sighashtype=None
    ):
        args = [hexstring, private_keys]
        if previous_transactions is not None or sighashtype is not None:
            args.append(previous_transactions or [])
            if sighashtype is not None:
                args.append(sighashtype)
        return self.proxy.signrawtransactionwithkey(*args)

    # Secure Messaging (SMSG), as registered by Verge Core v26.7.
    def smsgenable(self, walletname=None):
        return self.proxy.smsgenable() if walletname is None else self.proxy.smsgenable(walletname)

    def smsgdisable(self):
        return self.proxy.smsgdisable()

    def smsgoptions(self, *args):
        return self.proxy.smsgoptions(*args)

    def smsglocalkeys(self, *args):
        return self.proxy.smsglocalkeys(*args)

    def smsgscanchain(self):
        return self.proxy.smsgscanchain()

    def smsgscanbuckets(self):
        return self.proxy.smsgscanbuckets()

    def smsginfo(self):
        return self.proxy.smsginfo()

    def flushsmgsdb(self):
        return self.proxy.flushsmgsdb()

    def smsgaddaddress(self, address, pubkey):
        return self.proxy.smsgaddaddress(address, pubkey)

    def smsgaddlocaladdress(self, address):
        return self.proxy.smsgaddlocaladdress(address)

    def smsgimportprivkey(self, privkey, label=""):
        return self.proxy.smsgimportprivkey(privkey, label)

    def smsggetpubkey(self, address):
        return self.proxy.smsggetpubkey(address)

    def smsgsend(
        self,
        address_from,
        address_to,
        message,
        paid_msg=True,
        days_retention=31,
        testfee=False,
        fromfile=False,
        decodehex=False,
    ):
        return self.proxy.smsgsend(
            address_from,
            address_to,
            message,
            paid_msg,
            days_retention,
            testfee,
            fromfile,
            decodehex,
        )

    def smsgsendanon(self, address_to, message, days_retention=31):
        return self.proxy.smsgsendanon(address_to, message, days_retention)

    def smsginbox(self, mode="all", filter_=None):
        return self.proxy.smsginbox(mode) if filter_ is None else self.proxy.smsginbox(mode, filter_)

    def smsgoutbox(self, mode="all", filter_=None):
        return self.proxy.smsgoutbox(mode) if filter_ is None else self.proxy.smsgoutbox(mode, filter_)

    def smsgbuckets(self, mode="stats"):
        return self.proxy.smsgbuckets(mode)

    def smsgview(self):
        return self.proxy.smsgview()

    def smsg(self, msgid, options=None):
        return self.proxy.smsg(msgid) if options is None else self.proxy.smsg(msgid, options)

    def smsgpurge(self, msgid):
        return self.proxy.smsgpurge(msgid)
