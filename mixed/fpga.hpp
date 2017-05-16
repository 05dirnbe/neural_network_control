#ifndef FPGA_HPP
#define FPGA_HPP

#include <string>

#include "configuration.hpp"

namespace fpga {

    using namespace std;
    
    enum state { read, write, undefined };

    class FPGA_Operations {

        public:

            FPGA_Operations() : state(fpga::undefined){}

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
            FPGA_Adapter(const Operator ops ) : operations(ops) {}
            
        protected:
            Operator operations;
    };

    template < class Operator = FPGA_Operations >
    class FPGA: public FPGA_Adapter<Operator> {
       
        typedef FPGA_Adapter<Operator> super;

        public:

            FPGA() : FPGA_Adapter<Operator>( Operator() ) {}

            void write( const configuration::data_t data, const configuration::topic_key_t topic) {

                if (topic == "parameters"){
                    super::operations.prepare_write();
                    super::operations.write_parameters(data);
                    return;
                }
                else if (topic == "weights") {
                    super::operations.prepare_write();
                    super::operations.write_weights(data);
                    return;
                }
                else if (topic == "topology") {
                    super::operations.prepare_write();
                    super::operations.write_topology(data);
                    return;
                }
                else {
                    string msg("Error: Writing topic '" + topic + "' to FPGA not implemented.");
                    throw runtime_error(msg);
                    return;   
                }
            }

            const configuration::data_t read( const configuration::topic_key_t topic ) {

                super::operations.prepare_read();

                if (topic == "spikes"){
                    super::operations.prepare_read();
                    return super::operations.read_spikes();
                }
                else if (topic == "parameters") {
                    super::operations.prepare_read();
                    return super::operations.read_parameters();
                }
                else if (topic == "weights") {
                    super::operations.prepare_read();
                    return super::operations.read_weights();
                }
                else if (topic == "topology") {
                    super::operations.prepare_read();
                    return super::operations.read_topology();
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
