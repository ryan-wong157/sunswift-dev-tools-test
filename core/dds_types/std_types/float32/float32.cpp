#include "float32/float32.hpp"

Float32::Float32(float my_float) : my_float_{my_float} {}

float Float32::get_float() {
    return my_float_;
}

void Float32::set_float(float new_float) {
    my_float_ = new_float;
}