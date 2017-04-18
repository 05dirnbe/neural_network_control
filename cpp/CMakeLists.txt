cmake_minimum_required(VERSION 3.3)
project(controller)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
set(GCC_WARNINGS "-Wall")
set(GCC_OPTIMIZATION "-O3")
set(SOURCE_FILES controller.cpp)
set( CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} ${GCC_WARNINGS}" )
set( CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} ${GCC_OPTIMIZATION}" )

add_executable(controller ${SOURCE_FILES})
set( CMAKE_EXECUTABLE_SUFFIX ".exe")
   
# The following line will link with libzmq
TARGET_LINK_LIBRARIES( controller -lzmq)
