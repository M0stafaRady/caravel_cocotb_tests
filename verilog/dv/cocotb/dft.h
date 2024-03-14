#include <firmware_apis.h>


void GPIOs_waitLow_dft(unsigned int data){
    set_debug_reg1(0x74);
    // wait for data bit ignoring jtag bits 31 30 29 28 27
    unsigned int data_masked = data & 0x7FFFFFF;
    while(1){
        unsigned int read_data_masked = GPIOs_readLow() & 0x7FFFFFF;
        if (read_data_masked == data_masked)
            break;
    }
}
