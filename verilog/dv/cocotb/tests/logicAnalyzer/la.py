import cocotb
from cocotb.triggers import ClockCycles
import cocotb.log
from cocotb_includes import test_configure
from cocotb_includes import repot_test
from tests.common.debug_regs import DebugRegs


@cocotb.test()
@repot_test
async def la(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=415603)
    debug_regs = DebugRegs(caravelEnv)
    pass_list = (0x1B, 0x2B, 0x3B, 0x4B, 0x5B, 0x6B, 0x7B, 0x8B)
    fail_list = (0x1E, 0x2E, 0x3E, 0x4E, 0x5E, 0x6E, 0x7E, 0x8E)
    phases_fails = 8
    if int(caravelEnv.design_macros.LA_SIZE) < 128:
        phases_fails = 4
    phases_passes = 0
    reg1 = 0  # buffer
    # await ClockCycles(caravelEnv.clk,11200)
    while True:
        if debug_regs.read_debug_reg2() == 0xFF:  # test finish
            break
        if reg1 != debug_regs.read_debug_reg1():
            reg1 = debug_regs.read_debug_reg1()
            if reg1 in pass_list:  # pass phase
                phases_passes += 1
                phases_fails -= 1
                cocotb.log.info(f"[TEST] test passes phase {hex(reg1)[2]}")
            elif reg1 in fail_list:  # fail phase
                cocotb.log.error(
                    f"[TEST] test fails phase {hex(reg1)[2]} incorrect value recieved {hex(debug_regs.read_debug_reg2())}"
                )

        await ClockCycles(caravelEnv.clk, 1)

    if phases_fails != 0:
        cocotb.log.error(
            f"[TEST] finish with {phases_passes} phases passes and {phases_fails} phases fails"
        )
    else:
        cocotb.log.info(
            f"[TEST] finish with {phases_passes} phases passes and {phases_fails} phases fails"
        )

    await ClockCycles(caravelEnv.clk, 100)
