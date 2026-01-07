#include <iostream>
#include "dds_node.hpp"

DDSNode::DDSNode(std::string name, int age) : name_{name}, age_{age} {}

void DDSNode::print_deets() {
    std::cout << "Hello, I am " << name_ << " and I am " << age_ << " years old" << std::endl;
}
