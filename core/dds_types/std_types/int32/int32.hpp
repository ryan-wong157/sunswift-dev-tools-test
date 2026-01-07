#pragma once
#include <stdint.h>

class Int32 {
public:
    Int32(int32_t my_int = 0);
    int32_t get_int();
    void set_int(int32_t new_int);
private:
    int32_t my_int_ {};    
};