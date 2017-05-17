#ifndef FPGA_HPP
#define FPGA_HPP

#include <string>

#include "configuration.hpp"
#include <Eigen/Dense>

namespace fpga {

    using namespace std;
    using namespace Eigen;
    
    typedef configuration::topic_t topic_t;
    typedef configuration::command_t command_t;
    typedef configuration::value_t value_t;
    typedef configuration::matrix_t matrix_t;
    typedef Matrix< value_t, Dynamic, 1 > vector_t;

    enum state { read, write, undefined };

    template < typename M, typename T >
    const M generate_random_matrix(const unsigned int nrow, const unsigned int mcol){

        const MatrixXd m = (MatrixXd::Random(nrow,mcol) + MatrixXd::Ones(nrow,mcol) ) * 5;
        return m.cast< const T >();
    }

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

            const matrix_t read_weights() const {
                
                cout << "Reading weights from FPGA:" << endl;
               
                return generate_random_matrix<matrix_t, value_t>(2,2);
            }

            const matrix_t read_parameters() const {
                
                cout << "Reading parameters from FPGA:" << endl;
               
                return generate_random_matrix<matrix_t, value_t>(2,2);
            }

            const matrix_t read_spikes() const {
                
                cout << "Reading spikes from FPGA:" << endl;
           
                return generate_random_matrix<matrix_t, value_t>(2,2);
            }
  
            const matrix_t read_topology() const {
                
                cout << "Reading topology from FPGA:" << endl;
                
                return generate_random_matrix<matrix_t, value_t>(2,2);
            }

            const matrix_t read_empty() const {
            
                return matrix_t();
            }

            void write_parameters(const matrix_t & data ) const {
                cout << "Writing parameters to FPGA:" << endl;
                cout << data << endl;
            }

            void write_topology(const matrix_t & data ) const {
                cout << "Writing topology to FPGA:" << endl;
                cout << data << endl;
            }

            void write_weights(const matrix_t & data ) const {
                cout << "Writing weights to FPGA:" << endl;
                cout << data << endl;
            }

            void write_camera(const matrix_t & data ) const {
                cout << "Writing camera data to FPGA:" << endl;
                cout << data << endl;
            }

            void write_empty(const matrix_t & data) const {}

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

            void write( const matrix_t & data, const topic_t topic) {

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
                else if (topic == "camera") {
                    super::operations.prepare_write();
                    super::operations.write_camera(data);
                    return;
                }
                else {
                    string msg("Error: Writing topic '" + topic + "' to FPGA not implemented.");
                    throw runtime_error(msg);
                    return;   
                }
            }

            const matrix_t read( const topic_t topic ) {

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
