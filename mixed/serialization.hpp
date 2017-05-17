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

    typedef configuration::topic_t topic_t;
    typedef configuration::command_t command_t;
    typedef configuration::buffer_t buffer_t;
    typedef configuration::value_t value_t;
    typedef configuration::matrix_t matrix_t;
    typedef Matrix< value_t, Dynamic, 1 > vector_t;


    template < typename M, typename T >
    const M generate_random_matrix(const unsigned int nrow, const unsigned int mcol){

        const MatrixXd m = (MatrixXd::Random(nrow,mcol) + MatrixXd::Ones(nrow,mcol) ) * 5;
        return m.cast< const T >();
    }

    class Serializer_Operations {

        public:

            const matrix_t deserialize_matrix( buffer_t & buffer) const {
                
                const auto mat_restored = GetIntegerMatrix(buffer.data());

                const auto n_restored = mat_restored -> n();
                const auto m_restored = mat_restored -> m();
                const auto data_restored = mat_restored -> data();
                const auto data_size = data_restored -> Length();

                vector_t flat_data_restored(data_size);
                
                for (unsigned int i = 0; i < data_size; ++i)
                    flat_data_restored[i] =  data_restored->Get(i);
                
                const Map<matrix_t> matrix(flat_data_restored.data(), n_restored, m_restored);

                return matrix;
            }

            buffer_t serialize_matrix(const matrix_t data ) const {
                
                // auto matrix = generate_random_matrix<matrix_t, value_t>(2,3);

                auto matrix = data;

                const auto n = matrix.rows();
                const auto m = matrix.cols();
                const value_t * const flat_data = matrix.data();

                flatbuffers::FlatBufferBuilder builder(0);
                const auto data_vector = builder.CreateVector(flat_data, n * m );
                const auto mat = CreateIntegerMatrix(builder, n , m, data_vector);
                builder.Finish(mat);

                const auto buffer_pointer = builder.GetBufferPointer();
                const auto buffer_size = builder.GetSize();

                buffer_t data_buffer(buffer_size);

                memcpy( data_buffer.data(), buffer_pointer, buffer_size );

                return data_buffer;
            }

            const command_t deserialize_command( buffer_t& buffer) const {
                return string(static_cast<char*>(buffer.data()), buffer.size());
            }

            buffer_t serialize_command(const string & command ) const {
                
                buffer_t buffer(command.size());
                memcpy(buffer.data (), command.c_str(), command.size());
                
                return buffer;
            }

            buffer_t serialize_empty() const {
                buffer_t empty_buffer;
                return empty_buffer;
            }

            const matrix_t deserialize_empty_data() const {
                return matrix_t();
            }

            const command_t deserialize_empty_command() const {
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

            buffer_t serialize_data( const matrix_t & data, const topic_t topic) {

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
                else if (topic == "camera") {
                    return super::operations.serialize_matrix(data);
                }
                else {
                    string msg("Error: Serializing topic '" + topic + "' not implemented.");
                    throw runtime_error(msg);
                    return super::operations.serialize_empty();   
                }
            }

            const matrix_t deserialize_data( buffer_t & buffer, const topic_t topic) {

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
                else if (topic == "camera") {
                    return super::operations.deserialize_matrix(buffer);
                }
                else {
                    string msg("Error: Deserializing topic '" + topic + "' not implemented.");
                    throw runtime_error(msg);
                    return super::operations.deserialize_empty_data();   
                }
            }

            buffer_t serialize_command( const command_t & data, const topic_t topic) {

                if (topic == "command"){
                    return super::operations.serialize_command(data);
                }
                else {
                    string msg("Error: Serializing topic '" + topic + "' not implemented.");
                    throw runtime_error(msg);
                    return super::operations.serialize_empty();   
                }  
            }

            const command_t deserialize_command( buffer_t & buffer, const topic_t topic) {

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
