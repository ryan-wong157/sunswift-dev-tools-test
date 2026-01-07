#pragma once
#include <cstdint>

class Float32 {
public:
    Float32(float my_float = 0);
    float get_float();
    void set_float(float new_float);
private:
    float my_float_ {};    
};