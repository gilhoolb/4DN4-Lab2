import sys
import socket
from cryptography.fernet import Fernet
from server import *

class Client:

    # Set the server to connect to. If the server and client are running
    # on the same machine, we can use the current hostname.
    # SERVER_HOSTNAME = socket.gethostname()
    # SERVER_HOSTNAME = "192.168.1.22"
    SERVER_HOSTNAME = "localhost"
    
    # Try connecting to the compeng4dn4 echo server. You need to change
    # the destination port to 50007 in the connect function below.
    # SERVER_HOSTNAME = 'compeng4dn4.mooo.com'

    # RECV_BUFFER_SIZE = 5 # Used for recv.    
    RECV_BUFFER_SIZE = 1024 # Used for recv.



    def __init__(self):
        self.get_console_input()
        self.get_socket()
        self.connect_to_server()
        self.send_console_input_forever()

        #receive data from server
        #decrypt message
        #close conncetion
        #wait for another user command

    def get_socket(self):
        try:
            # Create an IPv4 TCP socket.
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Allow us to bind to the same port right away.            
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Bind the client socket to a particular address/port.
            # self.socket.bind((Server.HOSTNAME, 40000))
                
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def connect_to_server(self):
        try:
            # Connect to the server using its socket address tuple.
            self.socket.connect((Client.SERVER_HOSTNAME, Server.PORT))
            # print("Connected to \"{}\" on port {}".format(Client.SERVER_HOSTNAME, Server.PORT))
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def get_console_input(self):
        # In this version we keep prompting the user until a non-blank
        # line is entered, i.e., ignore blank lines.
        while True:
            student_id = input("Student_ID: ")
            cmd = input("CMD: ")
            self.input_text = student_id + "," + cmd
            print("Command entered: ", cmd)
            if self.input_text != "":
                break
        
        if cmd == "GMA":
            print("Fetching Midterm Average:")
        elif cmd == "GEA":
            print("Fetching Exam Average:")
        elif cmd == "GL1A":
            print("Fetching Lab 1 Average:")
        elif cmd == "GL2A":
            print("Fetching Lab 2 Average:")
        elif cmd == "GL3A":
            print("Fetching Lab 3 Average:")
        elif cmd== "GL4A":
            print("Fetching Lab 4 Average:")
        elif cmd == "GG":
            print("Fetching Student ", student_id, " grades:")
        else:
            print("GTFO with your invalid ass command bitch\n")
    
    def send_console_input_forever(self):
        while True:
            try:
                #self.get_console_input()
                self.connection_send()
                self.connection_receive()
                self.close_restart()
            except (KeyboardInterrupt, EOFError):
                print()
                print("Closing server connection ...")
                # If we get and error or keyboard interrupt, make sure
                # that we close the socket.
                self.socket.close()
                sys.exit(1)
                
    def connection_send(self):
        try:
            # Send string objects over the connection. The string must
            # be encoded into bytes objects first.
            self.socket.sendall(self.input_text.encode("utf-8"))
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def connection_receive(self):
        try:
            # Receive and print out text. The received bytes objects
            # must be decoded into string objects.
            recvd_bytes = self.socket.recv(Client.RECV_BUFFER_SIZE)

            # recv will block if nothing is available. If we receive
            # zero bytes, the connection has been closed from the
            # other end. In that case, close the connection on this
            # end and exit.
            if len(recvd_bytes) == 0:
                print("Closing server connection.")
                self.socket.close()
                sys.exit(1)

            # key = input("Data received, Please enter your encryption key: ")
            key = "M7E8erO15CIh902P8DQsHxKbOADTgEPGHdiY0MplTuY="
            fernet = Fernet(key)

            recvd_msg = fernet.decrypt(recvd_bytes)
            recvd_str = recvd_msg.decode("utf-8")
            print(recvd_str)


        except Exception as msg:
            print(msg)
            sys.exit(1)

    def close_restart(self):
        self.socket.close()
        print("\nSocket is disconnected.\n")
        self.get_console_input()
        self.get_socket()
        self.connect_to_server()


if __name__ == "__main__":
   Client()