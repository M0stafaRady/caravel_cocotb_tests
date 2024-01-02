#include <firmware_apis.h>


void main(){
    enable_debug();
    volatile char *dff2_start_address =  (volatile char *) DFF2_START_ADDR;
    volatile int dff2_size =  DFF2_SIZE;
    volatile char  data = 0x55;
    for (volatile int i = 0; i < dff2_size; i++){
      *(dff2_start_address+i) = data; 
    }
    for (volatile int i = 0; i < dff2_size; i++){
        if (data != *(dff2_start_address+i)){
            set_debug_reg2(dff2_start_address + i);
            set_debug_reg1(0x1E); 
            return;
        }
    }

    data = 0xAA;
    for (volatile int i = 0; i < dff2_size; i++){
      *(dff2_start_address+i) = data; 
    }
    for (volatile int i = 0; i < dff2_size; i++){
        if (data != *(dff2_start_address+i)){
            set_debug_reg2(dff2_start_address + i);
            set_debug_reg1(0x1E); 
            return;
        }
    }

    set_debug_reg1(0x1B);

}