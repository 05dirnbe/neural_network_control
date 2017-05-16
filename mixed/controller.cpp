# include <iostream>
# include <string>

# include <zmq.h>

# include "configuration.hpp"
# include "communication.hpp"
# include "fpga.hpp"
# include "serialization.hpp"
# include "controller.hpp"

using namespace std;
using namespace communication;
using namespace configuration;
using namespace controller;

int main(){

		
	// for (auto& it : write_commands) {
 //    	cout << it << endl;
	// }

	// cout << connections["controller"] << endl;
	// cout << ZMQ_REP << endl;
	
	// connect_socket(ZMQ_REP, connections["controller"]);

	// fpga::FPGA<> a;

	// parameters_t data = 10;

	// a.write(data, "topology");
	// cout << a.read("topology") << endl;

	// serialization::Serializer<> s;

	// cout << "serialized: " << s.serialize_data(data, "parameters") << endl;
	// cout << "deserialized: " << s.deserialize_data(100, "parameters") << endl;
	// cout << "serialized: " << s.serialize_command("quit", "command") << endl;
	// cout << "deserialized: " << s.deserialize_command(100, "command") << endl;
	// // cout << "deserialized:" << s

	Controller c;

	c.serve_forever();
}