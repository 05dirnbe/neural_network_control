#ifndef SERIALIZATION_HPP
#define SERIALIZATION_HPP

#include <string>
#include <zmq.hpp>

#include "configuration.hpp"


namespace serialization {

    using namespace std;

    
    class Serializer_Operations {

        public:

            const configuration::matrix_t deserialize_matrix( zmq::message_t & buffer) const {
                return 10;
            }

            zmq::message_t serialize_matrix(const configuration::matrix_t data ) const {
                zmq::message_t empty_buffer;
                return empty_buffer;
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
