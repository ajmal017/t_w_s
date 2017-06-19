import sys
import argparse
import datetime
import collections
import inspect

import logging
import time
import os.path

from ibapi import wrapper
from ibapi.client import EClient
from ibapi.utils import iswrapper

# types
from ibapi.common import *
from ibapi.order_condition import *
from ibapi.contract import *
from ibapi.order import *
from ibapi.order_state import *
from ibapi.execution import Execution
from ibapi.execution import ExecutionFilter
from ibapi.commission_report import CommissionReport
from ibapi.scanner import ScannerSubscription
from ibapi.ticktype import *

from ibapi.account_summary_tags import *

from ContractSamples import ContractSamples
from OrderSamples import OrderSamples
from AvailableAlgoParams import AvailableAlgoParams
from ScannerSubscriptionSamples import ScannerSubscriptionSamples
from FaAllocationSamples import FaAllocationSamples

class TestWrapper(wrapper.EWrapper):
    def __init__(self):
        wrapper.EWrapper.__init__(self)

# ! [socket_declare]
class TestClient(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)


class TestApp(TestWrapper, TestClient):
    def __init__(self):
        TestWrapper.__init__(self)
        TestClient.__init__(self, wrapper=self)

    @iswrapper
    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        super().contractDetails(reqId, contractDetails)
        print("ContractDetails. ReqId:", reqId, contractDetails.summary.symbol,
              contractDetails.summary.secType, "ConId:", contractDetails.summary.conId,
              "@", contractDetails.summary.exchange)

def main():
    app=TestApp()
    app.connect("127.0.0.1",7497,0)
    print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),app.twsConnectionTime()))

    # app.reqContractDetails(10, ContractSamples.SI())
    # app.reqMktData(1101,ContractSamples.SI(),"",False,False,[])
    # app.reqMktData(1101, ContractSamples.USStockAtSmart(), "", False, False, [])
    queryTime = (datetime.datetime.today() -datetime.timedelta(days=180)).strftime("%Y%m%d %H:%M:%S")
    SI_data=app.reqHistoricalData(4101, ContractSamples.SI(), queryTime,"1 M", "1 day", "MIDPOINT", 1, 1, [])
    app.run()
if __name__=="__main__":
    main()