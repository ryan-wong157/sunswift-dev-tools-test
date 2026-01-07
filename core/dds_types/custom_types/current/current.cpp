// change everything to current
#include "current/current.hpp"

// constructor
Current::Current(int32_t current) : current_(current) {}
int32_t Current::get_current() const {
    return current_;
}
void Current::set_current(int32_t current) {
    current_ = current;
}
