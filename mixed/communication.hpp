#ifndef COMMUNICATION_HPP
#define COMMUNICATION_HPP

#include "configuration.hpp"
#include <zmq.hpp>

namespace communication {

	using namespace std;
    using namespace zmq;

    context_t context(1);       // setting the context as a global variable is fine here

    inline socket_t bind_socket(const int socket_type, const string connection){

        // cout << "Binding " << configuration::socket_name[socket_type] << " to " << connection << endl;
        socket_t socket (context, socket_type);
        socket.bind (connection);

        return socket;
    }

    inline socket_t connect_socket(const int socket_type, const string connection){

        // cout << "Binding " << configuration::socket_name[socket_type] << " socket to " << connection << endl;
        socket_t socket(context, socket_type);
        socket.connect(connection);

        return socket;
    }
}

#endif	//COMMUNICATION_HPP
