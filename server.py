#!/usr/bin/python3

import socket
import sys
from cryptography.fernet import Fernet
from classroom import *



class  Server:
    HOST = "0.0.0.0"
    PORT = 50000

    RECV_BUFFER_SIZE = 1024
    MAX_BACKLOG = 10

    SOCKET_ADDR = (HOST, PORT)

    #encryption_key = Fernet.generate_key()
    #encryption_key = "bVE5-55Cgksfgg9VQBXjHEBiycWiodLT5_BmwHenKcQ="
    #encryption_key_bytes = encryption_key.encode('utf-8')
    #fernet = Fernet(encryption_key_bytes)

    def __init__(self):
        my_class = Classroom(class_file="course_grades_2023.csv")

        self.create_listen_socket()
        self.process_connections()
    
    

    def create_listen_socket(self):
        try:
            # Create  IPv4 socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Allow reuse without waiting for timeout
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

            # Bind Socket to host and port
            self.socket.bind(Server.SOCKET_ADDR)

            # Set socket to listen
            self.socket.listen(Server.MAX_BACKLOG)
            print("Listening on port {} ...".format(Server.PORT))
        except Exception as excpt:
            print(excpt)
            sys.exit(1)

    def process_connections(self):
        try:
            while True:
                self.connection_handler(self.socket.accept())
        except Exception as excpt:
            print(excpt)
        except KeyboardInterrupt:
            print()
        finally:
            self.socket.close()
            sys.exit(1)
    
    def connection_handler(self,  client):
        connection, address_port =  client
        print("*" *  70)
        print("Connection received from {}.".format(address_port))
        print(client)

        while True:
            try:
                # Receive bytes over TCP (blocking)
                recvd = connection.recv(Server.RECV_BUFFER_SIZE)

                # If 0 bytes received client connection has been closed
                if len(recvd) == 0:
                    print("Closing client connection ...")
                    connection.close()
                    break
                
                #Decode message  and print
                recvd_str =  recvd.decode("utf-8")
                print("Received: ", recvd_str)

                #self.my_class.process_request(recvd_str)

                #Encrypt result of above

                #send back to client

                #close connection

                #return to listen state

            except Exception:
                print("Error")
                sys.exit(1)

            

                
if __name__ == "__main__":
   Server()