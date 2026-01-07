// implement methods in voltage.hpp
#include "voltage/voltage.hpp"

// constructor
Voltage::Voltage(int32_t voltage) : voltage_(voltage) {}
int32_t Voltage::get_voltage() const {
    return voltage_;
}
void Voltage::set_voltage(int32_t voltage) {
    voltage_ = voltage;
}
