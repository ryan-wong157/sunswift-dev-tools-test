set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/bin) 
add_executable(app src/main.cpp src/funny_node.cpp)

SET (LIBS 
    std_types
    custom_types
    dds_node
)

target_include_directories(app PRIVATE include)
target_link_libraries(app PRIVATE ${LIBS})