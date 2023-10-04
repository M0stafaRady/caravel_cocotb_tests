#include <firmware_apis.h>

void stress_test_start(){
    flash_phy_clk_divisor_write(0);
    ManagmentGpio_outputEnable();
    ManagmentGpio_write(1);
}

void stress_test_end(){
    ManagmentGpio_write(0);
}