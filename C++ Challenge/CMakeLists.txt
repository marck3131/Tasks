cmake_minimum_required(VERSION 3.10)

# set the project name
project(CPP_task VERSION 1.0)

ADD_DEFINITIONS( -DHOME="${CMAKE_SOURCE_DIR}" )

# specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# add the executable
add_executable(CPP_task labyrinth.cpp)
