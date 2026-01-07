#include "int32/int32.hpp"

Int32::Int32(int32_t my_int) : my_int_{my_int} {}

int32_t Int32::get_int() {
    return my_int_;
}

void Int32::set_int(int32_t new_int) {
    my_int_ = new_int;
}