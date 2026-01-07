// TESTER
#include <string>

class DDSNode {
public:
    DDSNode(std::string name, int age);
    void print_deets();

private:
    std::string name_ {};
    int age_ {};    
};