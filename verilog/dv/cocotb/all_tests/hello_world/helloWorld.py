import cocotb
from all_tests.common.common import test_configure_dft
from caravel_cocotb.caravel_interfaces import report_test
from cocotb.triggers import ClockCycles


@cocotb.test()
@report_test
async def helloWorld(dut):
    caravelEnv = await test_configure_dft(dut)
    cocotb.log.info("[Test] Hello world")
    await ClockCycles(caravelEnv.clk, 100000)
