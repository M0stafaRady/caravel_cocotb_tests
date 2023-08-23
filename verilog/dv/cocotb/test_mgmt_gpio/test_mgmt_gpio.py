from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
import cocotb
from check_macro import CheckMacro


@cocotb.test()
@report_test
async def test_mgmt_gpio(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=28811)
    cocotb.log.info("[TEST] Start managment gpio test")
    await caravelEnv.wait_mgmt_gpio(1)
    cocotb.log.info("[TEST] Pass 1 at management gpio")
    CheckMacro(caravelEnv).check_macro()