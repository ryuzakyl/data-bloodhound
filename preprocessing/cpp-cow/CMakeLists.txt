cmake_minimum_required(VERSION 3.6)
project(cpp_cow)

set(CMAKE_CXX_STANDARD 11)

set(SOURCE_FILES src/alignment.h src/alignment.cpp)
add_library(_cpp_cow SHARED ${SOURCE_FILES})
