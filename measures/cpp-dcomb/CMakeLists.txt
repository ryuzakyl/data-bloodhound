cmake_minimum_required(VERSION 3.6)
project(cpp_dcomb)

set(CMAKE_CXX_STANDARD 11)

set(SOURCE_FILES src/dcomb.h src/dcomb.cpp)
add_library(_cpp_dcomb SHARED ${SOURCE_FILES})
