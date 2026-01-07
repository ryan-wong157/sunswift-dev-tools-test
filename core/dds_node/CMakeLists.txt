# Output path
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/lib) 

# Add all sources here
set(SRC_FILES 
    ${CMAKE_CURRENT_SOURCE_DIR}/dds_node.cpp
)

add_library(dds_node STATIC ${SRC_FILES})

target_include_directories(
    dds_node
    PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)