#ifndef FPGA_HPP
#define FPGA_HPP

#include <set>

#include "configuration.hpp"

namespace fpga {

    using namespace std;
    
    enum state { read, write, undefined };

    class FPGA_Operations {

        public:

            FPGA_Operations() : state(fpga::undefined) {}

            void prepare_read() {

                state = read;
            }

            void prepare_write() {

                state = write;
            }

            state get_state() const {
                return state;
            }

            const configuration::weights_t read_weights() const {
            
                return configuration::topics["weights"];
            }

            const configuration::parameters_t read_parameters() const {
            
                return configuration::topics["parameters"];
            }

            const configuration::spikes_t read_spikes() const {
            
                return configuration::topics["spikes"];
            }
  
            const configuration::topology_t read_topology() const {
            
                return configuration::topics["topology"];
            }

            const configuration::data_t read_empty() const {
            
                return configuration::topics["empty"];
            }

            void write_parameters(const configuration::parameters_t data ) const {
                cout << data << endl;
            }

            void write_topology(const configuration::topology_t data ) const {
                cout << data << endl;
            }

            void write_weights(const configuration::weights_t data ) const {
                cout << data << endl;
            }

            void write_empty(const configuration::data_t data) const {}

        private:

            state state;
    };


    template < class Operator >
    class FPGA_Adapter  {
       
        public:
            FPGA_Adapter(const set< const string> rc, const set< const string> wc, const map< const string, const unsigned int> t, const Operator ops ) :    
                            read_commands(rc),
                            write_commands(wc),
                            topics(t),
                            operations(ops)
                            {}
            
        protected:
            const set< const string> read_commands;
            const set< const string> write_commands;
            const map< configuration::topic_key_t, configuration::topic_value_t> topics;

            Operator operations;
    };

    template < class Operator = FPGA_Operations >
    class FPGA: public FPGA_Adapter<Operator> {
       
        typedef FPGA_Adapter<Operator> super;

        public:

            FPGA() : FPGA_Adapter<Operator>( configuration::read_commands , configuration::write_commands, configuration::topics, Operator() ) {}

            void write( const configuration::data_t data, const configuration::topic_key_t topic) {

                if (super::write_commands.find(topic) != super::write_commands.end()){

                    super::operations.prepare_write();

                    if (topic == "parameters"){
                        super::operations.write_parameters(data);
                        return;
                    }
                    else if (topic == "weights") {
                        super::operations.write_weights(data);
                        return;
                    }
                    else if (topic == "topology") {
                        super::operations.write_topology(data);
                        return;
                    }  
                }
                else {
                    string msg("Error: Writing topic '" + topic + "' from FPGA not implemented.");
                    throw runtime_error(msg);
                    return;
                }
            }

            const configuration::data_t read( const configuration::topic_key_t topic ) {

                if (super::read_commands.find(topic) != super::read_commands.end()){

                    super::operations.prepare_read();

                    if (topic == "spikes"){
                        return super::operations.read_spikes();
                    }
                    else if (topic == "parameters") {
                        return super::operations.read_parameters();
                    }
                    else if (topic == "weights") {
                        return super::operations.read_weights();
                    }
                    else if (topic == "topology") {
                        return super::operations.read_topology();
                    } 
                    else {
                        return super::operations.read_empty();
                    }
                }
                else {
                    string msg("Error: Reading topic '" + topic + "' from FPGA not implemented.");
                    throw runtime_error(msg);
                    return super::operations.read_empty();
                }
            }
    };
}

#endif	//FPGA_HPP
