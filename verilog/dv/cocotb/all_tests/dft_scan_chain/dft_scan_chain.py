import cocotb
from cocotb.triggers import ClockCycles
import cocotb.log
from all_tests.common.common import test_configure_dft
from caravel_cocotb.caravel_interfaces import report_test
from user_design import configure_userdesign
from dft import DFT
import random

@cocotb.test()
@report_test
async def dft_scan_chain(dut):
    caravelEnv = await test_configure_dft(dut, timeout_cycles=12396, is_test_mode=True)
    dft = DFT(caravelEnv)
    await dft.start_dft()
    # Generate a random number with 5600 bits
    vector = random.getrandbits(5600)
    await dft.shiftIR()
    await dft.drive_dft(vector)
    data_out = await dft.read_dft()
    if data_out != vector:
        cocotb.log.error(f"[DFT] read value {bin(data_out)} not equal to expected value {bin(vector)}")
    