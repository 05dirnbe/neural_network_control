# name: makefile for controller.cpp
# Authors: Michael Dirnberger
# Date: 10-05-17

# the compiler: gcc for C program, define as g++ for C++
CC = g++

# compiler flags:
#  -Wall turns on most, but not all, compiler warnings
#  -O3 enables aggressive compiler optimization
#  -std=c++11 enables c++11 syntax (auto, templates, ect)
CFLAGS  = -Wall -O3 -std=c++11
# define any directories containing header files other than /usr/include
ZMQ_INCLUDES = -L /usr/local/lib -lzmq
EIGEN_INCLUDES = -I /usr/local/include/eigen3
# the build target executable:
TARGET = controller

all: $(TARGET)

$(TARGET): $(TARGET).cpp
	$(CC) $(CFLAGS) $(ZMQ_INCLUDES) $(EIGEN_INCLUDES) -o $(TARGET) $(TARGET).cpp

commander:

	$(CC) $(CFLAGS) $(ZMQ_INCLUDES) -o commander commander.cpp

clean:
	$(RM) $(TARGET)