import cocotb
from cocotb.triggers import ClockCycles
import cocotb.log
from all_tests.common.common import test_configure_dft, isolate_mgmt_out
from caravel_cocotb.caravel_interfaces import report_test
from user_design import configure_userdesign
from dft import DFT
import random

@cocotb.test()
@report_test
async def dft_golden(dut):
    caravelEnv = await test_configure_dft(dut, timeout_cycles=526792, is_test_mode=False, num_error=60)
    dft = DFT(caravelEnv)
    vector_file = f'{cocotb.plusargs["USER_PROJECT_ROOT"]}/verilog/dv/cocotb/all_tests/dft_golden/mgmt_core_wrapper.vec.bin'.replace('"', '')
    out_file = f'{cocotb.plusargs["USER_PROJECT_ROOT"]}/verilog/dv/cocotb/all_tests/dft_golden/mgmt_core_wrapper.out.bin'.replace('"', '')
    chosen_numbers = random.sample(range(8, 278), 10)
    cocotb.log.info(f"[DFT] testing vectors {chosen_numbers}")
    await dft.start_dft()
    with open(vector_file, 'r') as vec_file, open(out_file, 'r') as golden_file:
        line_num = 0
        for vec, golden in zip(vec_file, golden_file):
            line_num += 1
            vec = clean_string(vec)
            golden = clean_string(golden)
            # cocotb.log.info(f"[DFT] testing vector {line_num} vec = {vec}")
            if line_num not in chosen_numbers:
                continue
            if not valid_vec(vec):
                continue
            await dft.test_vs_golden(f"line {line_num}", vec, golden)

    await ClockCycles(caravelEnv.clk, 10000)    

def valid_vec(vec):
    return all(c in ('0', '1', 'x') for c in vec)

def clean_string(s):
    s = s.replace('"', '')  # Remove double quotes
    s = s.replace("'", '')  # Remove single quotes
    s = s.replace('\t', '')  # Remove tabs
    s = s.replace('\n', '')  # Remove new lines
    s = s.replace(' ', '')  # Remove spaces
    return s