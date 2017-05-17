#ifndef CONFIGURATION_HPP
#define CONFIGURATION_HPP

#include <map>
#include <set>
#include <string>
#include <zmq.hpp>

namespace configuration {

	using namespace std;

    typedef const unsigned int matrix_t;
    typedef matrix_t data_t;

    typedef data_t parameters_t;
    typedef data_t weights_t;
    typedef data_t spikes_t;
    typedef data_t topology_t;
    typedef const string command_t;
    
    typedef zmq::message_t buffer_t;

    typedef command_t topic_key_t;
    typedef const unsigned int topic_value_t;

	const char *rc[] = {"read_weights", "read_parameters", "read_spikes", "read_topology"};
	const char *wc[] = {"write_weights", "write_parameters", "write_topology"};
	
	const set< command_t > read_commands(rc, rc + sizeof(rc) / sizeof(*rc));
	const set< command_t > write_commands(wc, wc + sizeof(wc) / sizeof(*wc));

	string desktop_ip("localhost");
	string raspberry_ip("localhost");
	string ip = raspberry_ip;
	
    map< topic_key_t, topic_value_t> topics = {
    { string("weights"), 1 },
    { string("parameters"), 2 },
    { string("spikes"), 3 },
    { string("topology"), 4 },
    { string("camera"), 5 },
    { string("command"), 6 },
    { string("empty"), 7 }};

    // these settings have worked in the pure python implementation to connect everything
	// map< command_t, const string> connections = {
 //    { string("commander"), string("tcp://" + ip + ":5555") },
 //    { string("controller"), string("tcp://" + ip + ":5555") },
 //    { string("input_data"), string("tcp://" + ip + ":5556") },
 //    { string("camera"), string("tcp://" + ip + ":5556") },
 //    { string("output_data"), string("tcp://" + ip + ":5557") },
 //    { string("monitor"), string("tcp://" + ip + ":5557") }};

    map< command_t, const string> connections = {
    { string("commander"), string("tcp://localhost:5555") },
    { string("controller"), string("tcp://*:5555") },
    { string("input_data"), string("tcp://localhost:5556") },
    { string("camera"), string("tcp://*:5556") },
    { string("output_data"), string("tcp://localhost:5557") },
    { string("monitor"), string("tcp://*:5557") }};


    const map< const unsigned int, const string> socket_name = {
    { 1, string("ZMQ_PUB") },
    { 2, string("ZMQ_SUB") },
    { 3, string("ZMQ_REQ") },
    { 4, string("ZMQ_REP") },
    { 5, string("ZMQ_DEALER") },
    { 6, string("ZMQ_ROUTER") }};  
}

#endif	//CONFIGURATION_HPP
