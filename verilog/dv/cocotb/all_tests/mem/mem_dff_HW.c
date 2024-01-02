#include <firmware_apis.h>


void main(){
    enable_debug();
    volatile short *dff_start_address =  (volatile short *) DFF1_START_ADDR;
    volatile int dff_size =  DFF1_SIZE / 2;
    volatile short data = 0x5555;
    for (volatile int i = 0; i < dff_size; i++){
      *(dff_start_address+i) = data; 
    }
    for (volatile int i = 0; i < dff_size; i++){
        if (data != *(dff_start_address+i)){
            set_debug_reg2(dff_start_address + i);
            set_debug_reg1(0x1E); 
            return;
        }
    }
    
    data = 0xAAAA;
    for (volatile int i = 0; i < dff_size; i++){
      *(dff_start_address+i) = data; 
    }
    for (volatile int i = 0; i < dff_size; i++){
        if (data != *(dff_start_address+i)){
            set_debug_reg2(dff_start_address + i);
            set_debug_reg1(0x1E); 
            return;
        }
    }
    
    set_debug_reg1(0x1B);
}