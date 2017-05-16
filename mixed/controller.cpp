# include <iostream>
# include <string>

# include <zmq.h>

# include "configuration.hpp"
# include "communication.hpp"
# include "fpga.hpp"

using namespace std;
using namespace communication;
using namespace configuration;

int main(){

	string s("blah");

	
	
	for (auto& it : write_commands) {
    	cout << it << endl;
	}

	cout << connections["controller"] << endl;
	cout << ZMQ_REP << endl;
	
	connect_socket(ZMQ_REP, connections["controller"]);

	fpga::FPGA<> a;

	parameters_t data = 10;

	a.write(data, "topology");
	cout << a.read("topology") << endl;

}