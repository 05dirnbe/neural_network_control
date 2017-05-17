#ifndef CONFIGURATION_HPP
#define CONFIGURATION_HPP

#include <map>
#include <set>
#include <string>
#include <zmq.hpp>
#include <Eigen/Dense>

namespace configuration {

	using namespace std;

    typedef int32_t value_t;
    typedef Eigen::Matrix< value_t, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor > matrix_t;
    typedef matrix_t data_t;

    typedef const string command_t;
    typedef command_t topic_t;
    typedef zmq::message_t buffer_t;

	const char *rc[] = {"read_weights", "read_parameters", "read_spikes", "read_topology"};
	const char *wc[] = {"write_weights", "write_parameters", "write_topology"};
	
	const set< command_t > read_commands(rc, rc + sizeof(rc) / sizeof(*rc));
	const set< command_t > write_commands(wc, wc + sizeof(wc) / sizeof(*wc));

	string desktop_ip("localhost");
	string raspberry_ip("localhost");
	string ip = raspberry_ip;
	
    map< topic_t, const unsigned int> topics = {
    { "weights", 1 },
    { "parameters", 2 },
    { "spikes", 3 },
    { "topology", 4 },
    { "camera", 5 },
    { "command", 6 },
    { "empty", 7 }};

    // these settings have worked in the pure python implementation to connect everything
	// map< const string, const string> connections = {
 //    { "commander", "tcp://" + ip + ":5555" },
 //    { "controller", "tcp://" + ip + ":5555" },
 //    { "input_data", "tcp://" + ip + ":5556" },
 //    { "camera", "tcp://" + ip + ":5556" },
 //    { "output_data", "tcp://" + ip + ":5557" },
 //    { "monitor", "tcp://" + ip + ":5557" }};

    map< const string, const string> connections = {
    { "commander", "tcp://localhost:5555" },
    { "controller", "tcp://*:5555" },
    { "input_data", "tcp://localhost:5556" },
    { "camera", "tcp://*:5556" },
    { "output_data", "tcp://localhost:5557" },
    { "monitor", "tcp://*:5557" }};


    const map< const unsigned int, const string> socket_name = {
    { 1, "ZMQ_PUB" },
    { 2, "ZMQ_SUB" },
    { 3, "ZMQ_REQ" },
    { 4, "ZMQ_REP" },
    { 5, "ZMQ_DEALER" },
    { 6, "ZMQ_ROUTER" }};  
}

#endif	//CONFIGURATION_HPP
