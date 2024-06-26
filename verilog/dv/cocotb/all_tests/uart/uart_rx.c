/*
 * SPDX-FileCopyrightText: 2020 Efabless Corporation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * SPDX-License-Identifier: Apache-2.0
 */

#include <firmware_apis.h>


// --------------------------------------------------------

void wait_for_char(char *c){
    
    if (UART_readChar() == *c){
        set_debug_reg2(0x1B); // recieved the correct character
    }else{
        set_debug_reg2(0x1E); // timeout didn't recieve the character
    }
    UART_popChar();
}

void main(){
    enable_debug();
    enableHkSpi(0);
    GPIOs_configure(6,GPIO_MODE_MGMT_STD_OUTPUT);
    GPIOs_configure(5,GPIO_MODE_MGMT_STD_INPUT_NOPULL);

    // Now, apply the configuration
    GPIOs_loadConfigs();


    UART_enableRX(1);

    set_debug_reg1(0xAA); // start sending B
    wait_for_char("B");

    set_debug_reg1(0xBB); // start sending M
    wait_for_char("M");

    set_debug_reg1(0xCC); // start sending A
    wait_for_char("A");

}
