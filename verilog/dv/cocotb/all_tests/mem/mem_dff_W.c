#include <firmware_apis.h>


void main(){
    enable_debug(); 
    volatile int *dff_start_address =  (volatile int *) DFF1_START_ADDR;
    volatile int dff_size =  DFF1_SIZE / 4;
    volatile short data = 0x5555;
    volatile int i;
    volatile int data_used;
    volatile int shifting;
    for (i = 0x0; i < dff_size; i++){
        shifting = 0xFFFFFFFF - (0x1 << i%32);
        data_used = 0x55555555 & shifting;
      *((volatile int *) dff_start_address+i) = data_used; 
    }
    for (i = 0x0; i < dff_size; i++){
        shifting = 0xFFFFFFFF - (0x1 << i%32);
        data_used = 0x55555555 & shifting;
        if (data_used != *((volatile int *) dff_start_address+i)){
            set_debug_reg2(dff_start_address+ i);
            set_debug_reg1(0x1E); 
            return;
        }
    }
    
    for (i = 0x0; i < dff_size; i++){
        shifting = 0xFFFFFFFF - (0x1 << i%32);
        data_used = 0xAAAAAAAA & shifting;
      *((volatile int *)dff_start_address+i) = data_used; 
    }
    for (i = 0x0; i < dff_size; i++){
        shifting = 0xFFFFFFFF - (0x1 << i%32);
        data_used = 0xAAAAAAAA & shifting;
        if (data_used != *((volatile int *)dff_start_address+i)){
            set_debug_reg2((volatile int *)dff_start_address+ i);
            set_debug_reg1(0x1E); 
            return;
        }
    }
    
    set_debug_reg1(0x1B);
}