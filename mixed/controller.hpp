#ifndef CONTROLLER_HPP
#define CONTROLLER_HPP

#include <iostream>
#include <string>
#include <zmq.hpp>
#include <stdlib.h>
// #include "zhelpers.hpp"

# include "configuration.hpp"
# include "communication.hpp"
# include "fpga.hpp"
# include "serialization.hpp"

namespace controller {

    using namespace std;
    using namespace zmq;
    using namespace communication;
    using namespace configuration;
    
    class Controller {

        public:

            Controller() :  commander(bind_socket(ZMQ_REP, connections["controller"])),
                            input_data(bind_socket(ZMQ_SUB, connections["camera"])),
                            output_data(bind_socket(ZMQ_PUB, connections["monitor"])),
                            command("pause")
                            {
                                // subscribe input data to everything
                                input_data.setsockopt(ZMQ_SUBSCRIBE,"");

                                // items[0].socket = input_data;
                                // items[0].events = ZMQ_POLLIN;

                                // items[1].socket = commander;
                                // items[1].events = ZMQ_POLLIN;
                            }

            static bool s_send (zmq::socket_t & socket, const std::string & string) {

                zmq::message_t message(string.size());
                memcpy (message.data(), string.data(), string.size());

                bool rc = socket.send (message);
                return (rc);
            }

            //  Sends string as 0MQ string, as multipart non-terminal
            static bool s_sendmore (zmq::socket_t & socket, const std::string & string) {

                zmq::message_t message(string.size());
                memcpy (message.data(), string.data(), string.size());

                bool rc = socket.send (message, ZMQ_SNDMORE);
                return (rc);
            }


            void serve_forever() {

                zmq::pollitem_t items [] = {
                    { commander, 0, ZMQ_POLLIN, 0 },
                    { input_data, 0, ZMQ_POLLIN, 0 }
                };

                while (true) {

                    try {

                        poll(&items[0], 2, 0);
                        
                        // first we poll the commander socket for arriving commands and associated payloads
                        if (items[0].revents & ZMQ_POLLIN) {
                                                    
                            commander.recv(&command_buffer);
                            commander.recv(&payload_buffer);
                            
                            command = serializer.deserialize_command(command_buffer, "command");

                            // string topic = "command";

                            // auto payload = serializer.deserialize_command(payload_buffer, topic);

                          


                            
                            
                            commander.send(serializer.serialize_command(command, "command"));

                        }
                        // if (items[1].revents & ZMQ_POLLIN) {
                        //     subscriber.recv(&message);
                        //     //  Process weather update
                        // }
                        
                        if (command == "quit") {
                            cout << "Recieved command: " << command << endl;
                            return ;
                        }

                        if (command != "pause") {
                            handle_command();
                            cout << "Executed command: " << command << endl;
                        } 


                        sleep(1);
                    
                    } catch (const std::exception & e) {


                        cout << e.what() << " Controller waiting for valid command." << endl;
                        command = "pause";
                    }
                }
            }

            const string get_topic_from_command( string s, string prefix) {

                return s.erase(s.find(prefix), prefix.size());
            } 

            void handle_command() {

                if (command.find("read_") != string::npos) {
                    
                    auto topic = get_topic_from_command(command, "read_");
                    auto read_data = fpga.read(topic);
                    auto topic_buffer = serializer.serialize_command(topic, "command");
                    auto read_data_buffer = serializer.serialize_data(read_data, topic);

                    //publish topic and data on output socket
                    output_data.send(topic_buffer, ZMQ_SNDMORE);
                    output_data.send(read_data_buffer);
                }

                if (command.find("write_") != string::npos) {
                    
                    auto topic = get_topic_from_command(command, "write_");
                    auto write_data = serializer.deserialize_data(payload_buffer, topic);
                    fpga.write(write_data, topic);
                    command = "pause";
                }


            }

            
        private:

            fpga::FPGA<> fpga;
            serialization::Serializer<> serializer;

            socket_t commander;
            socket_t input_data;
            socket_t output_data;

            string command;
            message_t command_buffer;
            message_t payload_buffer;
            
    };
}

#endif	//CONTROLLER_HPP
