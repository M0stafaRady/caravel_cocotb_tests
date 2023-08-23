import cocotb


class CheckMacro:
    def __init__(self, caravelEnv) -> None:
        self.user_hdl = caravelEnv.user_hdl

    def check_macro(self):
        if "USE_MACRO_1" in cocotb.plusargs:
            macro1 = self.user_hdl.macro_1.value.binstr
            if macro1 == "1":
                cocotb.log.info("Found USE_MACRO_1 effect")
            else:
                cocotb.log.error(f"Did not find USE_MACRO_1 effect {macro1}")
                return False

        if "USE_MACRO_2" in cocotb.plusargs:
            macro2 = self.user_hdl.macro_2.value.binstr
            if macro2 == "1":
                cocotb.log.info("Found USE_MACRO_2 effect")
            else:
                cocotb.log.error(f"Did not find USE_MACRO_2 effect {macro2}")
                return False
        return True
