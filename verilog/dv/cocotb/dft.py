from cocotb.triggers import Timer, ClockCycles, FallingEdge, RisingEdge
import cocotb
from cocotb.clock import Clock

class DFT():
    def __init__(self, caravelEnv):
        self.caravelEnv = caravelEnv
        self._signal_mapping()
    
    def _signal_mapping(self):
        self.caravelEnv.dut.gpio30_en.value = 1
        self.mode_en_hdl = self.caravelEnv.dut.gpio30
        self.caravelEnv.dut.gpio28_en.value = 1
        self.reset_hdl = self.caravelEnv.dut.gpio28
        self.caravelEnv.dut.gpio31_en.value = 1
        self.clock_hdl = self.caravelEnv.dut.gpio31
        self.caravelEnv.dut.gpio29_en.value = 1
        self.dft_in_hdl = self.caravelEnv.dut.gpio29
        self.dft_out_hdl = self.caravelEnv.dut.gpio27_monitor

    def enable_tms(self, is_enable):
        if is_enable:
            self.mode_en_hdl.value = 1
        else:
            self.mode_en_hdl.value = 0
    
    async def reset_dft(self):
        self.reset_hdl.value = 0
        await ClockCycles(self.clock_hdl, 1)
        self.reset_hdl.value = 1
        await ClockCycles(self.clock_hdl, 1)

    async def set_clock(self, period):
        clock_obj = Clock(
            self.clock_hdl, period, "ns"
        )  # Create a 25ns period clock on port clk
        cocotb.start_soon(clock_obj.start())  # Start the clock

    async def start_dft(self):
        clock = self.caravelEnv.get_clock_obj()
        period = clock.period / 1000
        await cocotb.start(self.set_clock(period))
        self.enable_tms(False)
        await ClockCycles(self.clock_hdl, 1)
        self.enable_tms(True)
        await self.reset_dft()
    
    async def drive_dft(self, data, length = 5600):
        for i in range(length):
            self.dft_in_hdl.value = data & 1
            await ClockCycles(self.clock_hdl, 1)
            data = data >> 1
    
    async def read_dft(self, length = 5600):
        data = 0
        cocotb.log.debug("[DFT] start reading DFT ")
        for i in range(length):
            await FallingEdge(self.clock_hdl)
            data = data | (self.dft_out_hdl.value.integer << i)
        return data

    async def shiftIR(self, instruction=0b0011, tms_pattern=0b01100110):
        for i in range(5):
            bit = tms_pattern & 1
            self.enable_tms(bit)
            await ClockCycles(self.clock_hdl, 1)
            tms_pattern = tms_pattern >> 1
        
        # At shift-IR: shift new instruction on tdi line
        for i in range(4):
            bit = instruction & 1
            self.dft_in_hdl.value = bit
            if i == 3:
                self.enable_tms(tms_pattern & 1) # exit ir
                tms_pattern = tms_pattern >> 1
            await ClockCycles(self.clock_hdl, 1)
            instruction = instruction >> 1
        
        for i in range(2):
            bit = tms_pattern & 1
            self.enable_tms(bit)
            await ClockCycles(self.clock_hdl, 1)
            tms_pattern = tms_pattern >> 1

        # enter shift-DR
        self.enable_tms(1)
        await ClockCycles(self.clock_hdl, 1)
        self.enable_tms(0)
        await ClockCycles(self.clock_hdl, 2)
            

    async def test_vs_golden(self, name: str, vector: str, golden_out: str):
        cocotb.log.info(f"[DFT] testing vector {name}")
        await self.shiftIR()
        vector = vector[::-1]
        golden_out = golden_out[::-1]
        vector_length = len(vector)
        cocotb.log.debug(f"[DFT] vector length = {vector_length}")
        for i in range(vector_length):
            self.dft_in_hdl.value = int(vector[i])
            if i == vector_length - 1:
                self.enable_tms(1)
            elif i == vector_length - 2:
                self.enable_tms(0)
            elif i == vector_length - 3:
                self.enable_tms(1)
            await ClockCycles(self.clock_hdl, 1)
        
        # shift DR
        self.enable_tms(0)
        await ClockCycles(self.clock_hdl, 1)
        
        # shift-out response
        golden_out_length = len(golden_out)
        cocotb.log.debug(f"[DFT] golden_out length = {golden_out_length}")
        errors = 0
        self.dft_in_hdl.value = 0
        for i in range(golden_out_length):
            await Timer(2, "ns")
            tdo = self.dft_out_hdl.value.binstr
            if tdo != golden_out[i] and golden_out[i] != "x":
                errors += 1
                cocotb.log.error(f"[DFT] error in vector {name} at reading bit {i} expected {golden_out[i]} got {tdo}")
            if i == golden_out_length - 1:
                self.enable_tms(1) # Exit-DR
            await ClockCycles(self.clock_hdl, 1)
        # update DR
        self.enable_tms(1)
        await ClockCycles(self.clock_hdl, 1)
        self.enable_tms(0) # run test idle
        await ClockCycles(self.clock_hdl, 1)  
        if errors != 0:
            cocotb.log.error(f"[DFT] {errors} errors in vector {name}")
        else:
            cocotb.log.info(f"[DFT] vector {name} passed")
        self.enable_tms(1)
        