// #include <zmq.hpp>
// #include <iostream>

#include <zmq.hpp>
#include <string>
#include <iostream>

#include <unistd.h>



int main() {
    //  Prepare our context and socket
    zmq::context_t context(1);
    zmq::socket_t socket(context, ZMQ_PAIR);
    socket.bind("tcp://*:5555");

    // forever loop
    while (true) {
        zmq::message_t request;

        //  Wait for next request from client
        socket.recv(&request);
        int replyMessage = int(static_cast<int *>(request.data()));
        // Print out received message
        std::cout << "Received from client: " << replyMessage << std::endl;

        //  See the gradual sending/replying from client
        sleep(1);

        zmq::message_t reply(request.size());
        memcpy(reply.data(), request.data(), request.size());
        socket.send(reply);
    }
    return 0;
}