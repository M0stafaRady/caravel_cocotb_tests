#include <firmware_apis.h>

void main(){
    ManagmentGpio_write(0);
    ManagmentGpio_outputEnable();
    ManagmentGpio_write(1);
    return;
}