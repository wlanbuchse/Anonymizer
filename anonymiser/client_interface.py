import socket
from anonymiser.processor import Processor
from anonymiser.user_agent_manager import UserAgentManager

__author__ = 'johannes'


class ClientInterface:
    """
    This class is responsible for handling incoming data from clients (browsers). It spawns a new instance (thread) of
    the processor-class for each unique client.
    """

    def __init__(self):
        # The program will be listening on port 8008 on localhost
        self.address = ('localhost', 8008)
        # This list will hold every active connection so that there is always only one processor-instance for each
        # unique client. The methods register() and deregister() use this variable.
        self.proc_register = []
        self.listener_running = False
        self.user_agent_manager = UserAgentManager()

    def start(self):
        """
        Starts the listener on localhost on the port specified in the constructor (s.a.)
        """

        self.start_listener()

    def start_listener(self):
        """
        This starts listening on the specified port (s.a.). Accepts connections in a loop creating new processor-threads
        for each unique client.
        """

        # Create socket
        self.listener_running = True
        listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener_socket.bind(self.address)
        listener_socket.listen(1)

        print('[I] Now listening for incoming requests on port ' + str(self.address[1]))

        while self.listener_running:
            connection, address = listener_socket.accept()
            # Start a new processor-thread to handle this connection
            # The processor-constructor only spawns a new instance if there is no other instance handling this client
            thread = Processor(self, address, connection)
            thread.start()

    def register(self, address):
        """
        This method is used by processor-instances (threads) to let the client-interface know they exist so that the
        client-interface doesn't spawn two instances (threads) of the processor-class for the same client.
        Uses the proc_register variable of the client_interface-class (this class)
        """

        if address in self.proc_register:
            # This lets the caller know that there already is an instance handling that connection and that he can shut
            # down.
            return -1
        else:
            self.proc_register.append(address)
            return 1

    def deregister(self, address):
        """
        This method is used by processor-instances (threads) to let the client-interface know that they are finished
        and are shutting down so that the processor-class can spawn a new instance (thread) for a particular client.
        """

        if address not in self.proc_register:
            return -1
        else:
            self.proc_register.remove(address)
            return 1
