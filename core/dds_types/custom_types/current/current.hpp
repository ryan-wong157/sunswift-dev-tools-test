#pragma once
#include <cstdint>
// change everythign to current
class Current {
// Stores an int32 current and exposes getter and setter methods. This is JUST the interface.
// use snake_case for everything
public:
    Current(int32_t current = 0);

    // Getter for current
    int32_t get_current() const;

    // Setter for current
    void set_current(int32_t current);
private:
    int32_t current_;
};