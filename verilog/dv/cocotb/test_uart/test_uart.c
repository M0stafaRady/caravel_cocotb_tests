#include <firmware_apis.h>

void main(){
    ManagmentGpio_write(0);
    ManagmentGpio_outputEnable();
    UART_enableTX(1);
    ManagmentGpio_write(1); // configuration finished 

    print("Hi\n");
    return;
}