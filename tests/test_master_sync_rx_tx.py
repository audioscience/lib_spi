#!/usr/bin/env python
import xmostest
from spi_master_checker import SPIMasterChecker
import os


def do_rx_tx_sync(burnt_threads, cb_enabled, miso_enabled, mosi_enable):
    resources = xmostest.request_resource("xsim")

    xmostest.build('spi_master_sync_rx_tx', build_config="{burnt}{cb}{miso}{mosi}".format(burnt=burnt_threads,cb=cb_enabled,miso=miso_enabled,mosi=mosi_enable))

    binary = "spi_master_sync_rx_tx/bin/{burnt}{cb}{miso}{mosi}/spi_master_sync_rx_tx_{burnt}{cb}{miso}{mosi}.xe".format(burnt=burnt_threads,cb=cb_enabled,miso=miso_enabled,mosi=mosi_enable)


    checker = SPIMasterChecker("tile[0]:XS1_PORT_1C",
                               "tile[0]:XS1_PORT_1D",
                               "tile[0]:XS1_PORT_1A",
                               ["tile[0]:XS1_PORT_1B"],
                               "tile[0]:XS1_PORT_1E",
                               "tile[0]:XS1_PORT_16B")

    tester = xmostest.ComparisonTester(open('master.expect'),
                                     'lib_spi', 
                                     'spi_master_sim_tests',
                                     'spi_master_sync_rx_tx_{burnt}{cb}{miso}{mosi}'.format(burnt=burnt_threads,cb=cb_enabled,miso=miso_enabled,mosi=mosi_enable), 
                                     regexp=True)

    xmostest.run_on_simulator(resources['xsim'], binary,
                              simthreads = [checker],
                              #simargs=['--vcd-tracing', '-o ./spi_master_sync_rx_tx/trace.vcd -tile tile[0] -pads -functions -ports -instructions'],
                              simargs=[],
                              suppress_multidrive_messages = False,
                              tester = tester)

def runtest():
    for burnt_threads in [3, 7]:
      for cb_enabled in [0, 1]:
        for miso_enabled in [0, 1]:
          for mosi_enabled in [0, 1]:
            if (miso_enabled==1 or (miso_enabled==1)):
              do_rx_tx_sync(burnt_threads, cb_enabled, miso_enabled, mosi_enabled)