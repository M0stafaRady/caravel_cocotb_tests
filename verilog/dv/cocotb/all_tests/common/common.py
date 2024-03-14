import cocotb
from caravel_cocotb.interfaces.common_functions.test_functions import read_config_file, test_configure


from cocotb.triggers import ClockCycles

async def test_configure_dft(dut: cocotb.handle.SimHandle,
    timeout_cycles=1000000,
    clk=read_config_file()['clock'],
    timeout_precision=0.2,
    num_error=int(read_config_file()['max_err']),
    start_up=True):
    disable_jtag_testmode(dut)
    caravelEnv = await test_configure(dut, timeout_cycles, clk, timeout_precision, num_error, start_up=False)
    # manual start udisable_jtag_testmodep
    await caravelEnv.power_up()
    await caravelEnv.disable_csb()  # no need for this anymore as default for gpio3 is now pullup
    await caravelEnv.reset()
    await caravelEnv.disable_bins(ignore_bins=[3, 4, 28, 29, 30, 31])
    await ClockCycles(caravelEnv.clk, 10)
    return caravelEnv

def disable_jtag_testmode(dut):
    dut.gpio28_en.value = 1
    dut.gpio28.value = 0
    dut.gpio29_en.value = 1
    dut.gpio29.value = 0
    dut.gpio30_en.value = 1
    dut.gpio30.value = 0
    dut.gpio31_en.value = 1
    dut.gpio31.value = 0