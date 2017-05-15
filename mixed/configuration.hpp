#ifndef CONFIGURATION_HPP
#define CONFIGURATION_HPP

#include <map>
#include <set>
#include <string>

namespace configuration {

	using namespace std;

	const char *rc[] = {"read_weights", "read_parameters", "read_spikes", "read_topology"};
	const char *wc[] = {"write_weights", "write_parameters", "write_topology"};
	
	enum topics { weights, parameters, spikes, topology, camera, command };

	const set< const string> read_commands(rc, rc + sizeof(rc) / sizeof(*rc));
	const set< const string> write_commands(wc, wc + sizeof(wc) / sizeof(*wc));

	string desktop_ip("localhost");
	string raspberry_ip("localhost");
	string ip = raspberry_ip;
	
	std::map<std::string, string> connections = {
    { string("commander"), string("tcp://" + ip + ":5555") },
    { string("controller"), string("tcp://" + ip + ":5555") },
    { string("input_data"), string("tcp://" + ip + ":5556") },
    { string("camera"), string("tcp://" + ip + ":5556") },
    { string("output_data"), string("tcp://" + ip + ":5557") },
    { string("monitor"), string("tcp://" + ip + ":5557") }};

    std::map<int, string> socket_name = {
    { 1, string("ZMQ_PUB") },
    { 2, string("ZMQ_SUB") },
    { 3, string("ZMQ_REQ") },
    { 4, string("ZMQ_REP") },
    { 5, string("ZMQ_DEALER") },
    { 6, string("ZMQ_ROUTER") }};

}

#endif	//CONFIGURATION_HPP
