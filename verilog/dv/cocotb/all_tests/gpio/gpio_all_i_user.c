#include <common.h>



void main(){
    enable_debug();
    enableHkSpi(0);
    GPIOs_configureAll(GPIO_MODE_USER_STD_INPUT_NOPULL);
    GPIOs_loadConfigs();      
    output_enable_all_gpio_user(0);
    // low
    wait_over_input_l(0xAA,0xFFFFFFFF);
    wait_over_input_l(0XBB,0xAAAAAAAA);
    wait_over_input_l(0XCC,0x55555555);
    wait_over_input_l(0XDD,0x0);
    // high
    wait_over_input_h(0XD1,0x3F);
    wait_over_input_h(0XD2,0x0);
    wait_over_input_h(0XD3,0x15);
    wait_over_input_h(0XD4,0x2A);

    // trying to inject error by sending data to gpio by firmware where gpios configured as input 
    set_debug_reg1(0XD5);
    set_debug_reg1(0XD5); // for delay insertion for release
    GPIOs_writeLow(0x5AE1FFB8); // random number
    GPIOs_writeHigh(0x1E); // random number
    set_debug_reg2(0xFF);
}

void wait_over_input_l(unsigned int start_code, unsigned int exp_val){
    set_debug_reg1(start_code); // configuration done wait environment to send exp_val to reg_mprj_datal
    wait_gpio_user_l(exp_val);
    set_debug_reg2(get_gpio_user_l());

}
void wait_over_input_h(unsigned int start_code, unsigned int exp_val){
    set_debug_reg1(start_code); 
    wait_gpio_user_h(exp_val);
    set_debug_reg2(get_gpio_user_h());
}