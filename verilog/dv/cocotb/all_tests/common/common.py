import cocotb
from caravel_cocotb.interfaces.common_functions.test_functions import read_config_file, test_configure

from cocotb.handle import Force
from cocotb.triggers import ClockCycles

async def test_configure_dft(dut: cocotb.handle.SimHandle,
    timeout_cycles=1000000,
    clk=read_config_file()['clock'],
    timeout_precision=0.2,
    num_error=int(read_config_file()['max_err']),
    start_up=True, is_test_mode=False):
    if not is_test_mode:
        disable_dft_testmode(dut)
    caravelEnv = await test_configure(dut, timeout_cycles, clk, timeout_precision, num_error, start_up=False)
    # manual start udisable_jtag_testmodep
    await caravelEnv.power_up()
    await caravelEnv.disable_csb()  # no need for this anymore as default for gpio3 is now pullup
    await caravelEnv.reset()
    await caravelEnv.disable_bins(ignore_bins=[3, 4, 28, 29, 30, 31])
    await ClockCycles(caravelEnv.clk, 10)
    return caravelEnv

def disable_dft_testmode(dut):
    dut.gpio28_en.value = 1
    dut.gpio28.value = 0
    dut.gpio29_en.value = 1
    dut.gpio29.value = 0
    dut.gpio30_en.value = 1
    dut.gpio30.value = 0
    dut.gpio31_en.value = 1
    dut.gpio31.value = 0

def isolate_mgmt_out(dut):
    mgmt_hdl = dut.uut.chip_core.soc
    mgmt_hdl.debug_mode.value = Force(0)
    mgmt_hdl.debug_oeb.value = Force(0)
    mgmt_hdl.debug_out.value = Force(0)
    mgmt_hdl.flash_clk.value = Force(0)
    mgmt_hdl.flash_csb.value = Force(0)
    mgmt_hdl.flash_io0_do.value = Force(0)
    mgmt_hdl.flash_io0_oeb.value = Force(0)
    
    # mgmt_hdl.flash_io1_do.value = Force(0)
    # mgmt_hdl.flash_io1_oeb.value = Force(0)
    # mgmt_hdl.flash_io2_do.value = Force(0)
    # mgmt_hdl.flash_io2_oeb.value = Force(0)
    # mgmt_hdl.flash_io3_do.value = Force(0)
    # mgmt_hdl.flash_io3_oeb.value = Force(0)

    mgmt_hdl.gpio_inenb_pad.value = Force(0)
    mgmt_hdl.gpio_mode0_pad.value = Force(0)
    mgmt_hdl.gpio_mode1_pad.value = Force(0)
    mgmt_hdl.gpio_out_pad.value = Force(0)
    mgmt_hdl.gpio_outenb_pad.value = Force(0)
    mgmt_hdl.hk_cyc_o.value = Force(0)
    mgmt_hdl.hk_stb_o.value = Force(0)
    mgmt_hdl.la_iena.value = Force(0)
    mgmt_hdl.la_oenb.value = Force(0)
    mgmt_hdl.la_output.value = Force(0)
    mgmt_hdl.mprj_adr_o.value = Force(0)
    mgmt_hdl.mprj_cyc_o.value = Force(0)
    mgmt_hdl.mprj_dat_o.value = Force(0)
    mgmt_hdl.mprj_sel_o.value = Force(0)
    mgmt_hdl.mprj_stb_o.value = Force(0)
    mgmt_hdl.mprj_wb_iena.value = Force(0)
    mgmt_hdl.mprj_we_o.value = Force(0)
    mgmt_hdl.qspi_enabled.value = Force(0)
    mgmt_hdl.ser_tx.value = Force(0)
    mgmt_hdl.spi_csb.value = Force(0)
    mgmt_hdl.spi_enabled.value = Force(0)
    mgmt_hdl.spi_sck.value = Force(0)
    mgmt_hdl.spi_sdo.value = Force(0)
    mgmt_hdl.spi_sdoenb.value = Force(0)
    mgmt_hdl.trap.value = Force(0)
    mgmt_hdl.uart_enabled.value = Force(0)
    mgmt_hdl.user_irq_ena.value = Force(0)