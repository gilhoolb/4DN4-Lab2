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

    def __init__(self):
        self.my_class = Classroom(class_file="course_grades_2023.csv")

        self.create_listen_socket()
        self.process_connections()
    
    

    def create_listen_socket(self):
        # try:
            # Create  IPv4 socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Allow reuse without waiting for timeout
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

            # Bind Socket to host and port
            self.socket.bind(Server.SOCKET_ADDR)

            # Set socket to listen
            self.socket.listen(Server.MAX_BACKLOG)
            print("Listening on port {} ...".format(Server.PORT))
        # except Exception as excpt:
        #     print(excpt)
        #     sys.exit(1)

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

        while True:
            try:
                # Receive bytes over TCP (blocking)
                recvd = connection.recv(Server.RECV_BUFFER_SIZE)

                # If 0 bytes received client connection has been closed
                if len(recvd) == 0:
                    print("Closing client connection ...")
                    connection.close()
                    print("Listening on port {} ...".format(Server.PORT))
                    break
                
                #Decode message  and print
                recvd_str = recvd.decode("utf-8")
                recvd_str =  recvd_str.split(',')
                recvd_str[0] = recvd_str[0].strip()
                recvd_str[1] = recvd_str[1].strip()

                if (int(recvd_str[0]) in self.my_class.students):
                    print("User", recvd_str[0], "found!")
                else:
                    print("User", recvd_str[0], "not found!")
                    connection.close()
                    print("Listening on port {} ...".format(Server.PORT))
                    break
                
                if (recvd_str[1] in {"GMA", "GEA", "GL1A", "GL2A", "GL3A", "GL4A", "GG"}):
                    print("CMD", recvd_str[1], "found!")
                else:
                    print("CMD", recvd_str[1], "not found!")
                    connection.close()
                    print("Listening on port {} ...".format(Server.PORT))
                    break

                print("Received cmd:", recvd_str[1], "for student:", recvd_str[0])

                result = self.my_class.process_request(recvd_str)
                print(result)
                #Encrypt result of above
                key = getattr(self.my_class.students[int(recvd_str[0])], "key")
                key_bytes = key.encode("utf-8")
                fernet  = Fernet(key_bytes)
                encrypted_message = fernet.encrypt(result.encode("utf-8"))

                #send back to client
                connection.sendall(encrypted_message)

            except Exception as ass:
                print("Error:",ass)
                sys.exit(1)

            

                
if __name__ == "__main__":
   Server()