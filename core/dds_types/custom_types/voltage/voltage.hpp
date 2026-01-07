#pragma once
#include <cstdint>
class Voltage {
// Stores an int32 voltage and exposes getter and setter methods. This is JUST the interface.
// use snake_case for everything
public:
    Voltage(int32_t voltage = 0);

    // Getter for voltage
    int32_t get_voltage() const;

    // Setter for voltage
    void set_voltage(int32_t voltage);
private:
    int32_t voltage_;
};