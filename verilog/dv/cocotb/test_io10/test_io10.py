from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
import cocotb
from cocotb.triggers import ClockCycles
@cocotb.test()
@report_test
async def test_io10(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=81)
    caravelEnv.drive_gpio_in(20, 1)
    await ClockCycles(caravelEnv.clk, 10)
    rev1 = caravelEnv.monitor_gpio(10)
    caravelEnv.drive_gpio_in(20, 0)
    await ClockCycles(caravelEnv.clk, 10)
    rev2 = caravelEnv.monitor_gpio(10)
    if rev1 == 1 and rev2 == 0:
        cocotb.log.info("Test passed")
    else:
        cocotb.log.error("Test failed")