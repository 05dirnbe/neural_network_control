#ifndef SERIALIZATION_HPP
#define SERIALIZATION_HPP

#include <string>
#include <zmq.hpp>
#include <Eigen/Dense>

#include "configuration.hpp"
#include "cpp_buffer_specifications_generated.h"


namespace serialization {

    using namespace std;
    using namespace Buffer;
    using namespace Eigen;

    typedef int32_t value_t;
    typedef uint8_t buffer_t;
    typedef Matrix< value_t, Dynamic, Dynamic, RowMajor > matrix_t;
    typedef Matrix< value_t, Dynamic, 1 > vector_t;


    template < typename M, typename T >
    const M generate_matrix(const unsigned int nrow, const unsigned int mcol){

        const MatrixXd m = (MatrixXd::Random(nrow,mcol) + MatrixXd::Ones(nrow,mcol) ) * 5;
        return m.cast< const T >();
    }

    class Serializer_Operations {

        public:

            const configuration::matrix_t deserialize_matrix( zmq::message_t & buffer) const {
                
                const auto mat_restored = GetIntegerMatrix(buffer.data());

                const auto n_restored = mat_restored -> n();
                const auto m_restored = mat_restored -> m();
                const auto data_restored = mat_restored -> data();
                const auto data_size = data_restored -> Length();

                vector_t flat_data_restored(data_size);
                
                for (unsigned int i = 0; i < data_size; ++i)
                    flat_data_restored[i] =  data_restored->Get(i);

                
                // cout << "restored n to: " << n << endl;
                // cout << "restored m to: " << m << endl;
                // cout << "restored data has size: " << data_size << endl;

                // cout << "data restored to : \n" << flat_data_restored << endl;
                
                const Map<matrix_t> matrix_restored(flat_data_restored.data(), n_restored, m_restored);

                // cout << matrix_restored << endl;

                return 10;
            }

            zmq::message_t serialize_matrix(const configuration::matrix_t data ) const {
                
                auto matrix = generate_matrix<matrix_t, value_t>(2,3);

                const auto n = matrix.rows();
                const auto m = matrix.cols();
                const value_t * const flat_data = matrix.data();

                flatbuffers::FlatBufferBuilder builder(0);
                const auto data_vector = builder.CreateVector(flat_data, n * m );
                const auto mat = CreateIntegerMatrix(builder, n , m, data_vector);
                builder.Finish(mat);

                const auto buffer_pointer = builder.GetBufferPointer();
                const auto buffer_size = builder.GetSize();

                zmq::message_t data_buffer(buffer_size);

                memcpy( data_buffer.data(), buffer_pointer, buffer_size );

                return data_buffer;
            }

            const configuration::command_t deserialize_command( zmq::message_t& buffer) const {
                return string(static_cast<char*>(buffer.data()), buffer.size());
            }

            zmq::message_t serialize_command(const string & command ) const {
                
                zmq::message_t buffer(command.size());
                memcpy(buffer.data (), command.c_str(), command.size());
                
                return buffer;
            }

            zmq::message_t serialize_empty() const {
                zmq::message_t empty_buffer;
                return empty_buffer;
            }

            const configuration::data_t deserialize_empty_data() const {
                return 0;
            }

            const configuration::command_t deserialize_empty_command() const {
                return 0;
            }
    };


    template < class Operator >
    class Serializer_Adapter  {
       
        public:
            Serializer_Adapter(const Operator ops ) : operations(ops) {}
            
        protected:
            Operator operations;
    };

    template < class Operator = Serializer_Operations >
    class Serializer: public Serializer_Adapter<Operator> {
       
        typedef Serializer_Adapter<Operator> super;

        public:

            Serializer() : Serializer_Adapter<Operator>( Operator() ) {}

            zmq::message_t serialize_data( const configuration::data_t & data, const configuration::topic_key_t topic) {

                if (topic == "spikes"){
                    return super::operations.serialize_matrix(data);
                }
                else if (topic == "weights") {
                    return super::operations.serialize_matrix(data);
                }
                else if (topic == "parameters") {
                    return super::operations.serialize_matrix(data);
                }
                else if (topic == "topology") {
                    return super::operations.serialize_matrix(data);
                }
                else {
                    string msg("Error: Serializing topic '" + topic + "' not implemented.");
                    throw runtime_error(msg);
                    return super::operations.serialize_empty();   
                }
            }

            configuration::data_t deserialize_data( zmq::message_t & buffer, const configuration::topic_key_t topic) {

                if (topic == "spikes"){
                    return super::operations.deserialize_matrix(buffer);
                }
                else if (topic == "weights") {
                    return super::operations.deserialize_matrix(buffer);
                }
                else if (topic == "parameters") {
                    return super::operations.deserialize_matrix(buffer);
                }
                else if (topic == "topology") {
                    return super::operations.deserialize_matrix(buffer);
                }
                else {
                    string msg("Error: Deserializing topic '" + topic + "' not implemented.");
                    throw runtime_error(msg);
                    return super::operations.deserialize_empty_data();   
                }
            }

            zmq::message_t serialize_command( const string & data, const configuration::topic_key_t topic) {

                if (topic == "command"){
                    return super::operations.serialize_command(data);
                }
                else {
                    string msg("Error: Serializing topic '" + topic + "' not implemented.");
                    throw runtime_error(msg);
                    return super::operations.serialize_empty();   
                }  
            }

            const string deserialize_command( zmq::message_t & buffer, const configuration::topic_key_t topic) {

                if (topic == "command"){
                    return super::operations.deserialize_command(buffer);
                }
                else {
                    string msg("Error: Deserializing topic '" + topic + "' not implemented.");
                    throw runtime_error(msg);
                    return super::operations.deserialize_empty_command();   
                }  
            } 


    };
}

#endif	//SERIALIZATION_HPP
