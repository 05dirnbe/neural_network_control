
#include <zmq.hpp>
#include <string>
#include <iostream>

#include "serialization.hpp"
// #include "zhelpers.hpp"

using namespace std;

int main () {
    
    serialization::Serializer<> serializer;

    //  Prepare our context and socket
    zmq::context_t context (1);
    zmq::socket_t socket (context, ZMQ_REQ);
    socket.bind ("tcp://*:5555");



    // string command = "write_spikes";
    // string command = "read_topology";
    string command = "quit";
    string payload = "payload";
    string topic = "command";
    
    auto command_buffer = serializer.serialize_command(command, "command");
    auto payload_buffer = serializer.serialize_command(payload, topic);
    
    socket.send(command_buffer, ZMQ_SNDMORE);
    socket.send(payload_buffer);

    
    socket.recv(&command_buffer);

    auto reply = serializer.deserialize_command(command_buffer, "command");

    cout << "Acknowledges command: " << reply << endl;

    return 0;
}
