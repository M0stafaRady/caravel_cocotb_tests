#include <firmware_apis.h>

void main(){
    // dummy code to keep the cpu running 
    int x = 0;
    for (int i = 0; i < 100000; i++){
        if (i%2 == 0)
            x = x+2;
        else
            x = x+1;
    }
}