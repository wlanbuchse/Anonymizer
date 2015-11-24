from anonymiser.request_parser import RequestParser
from anonymiser.request_builder import RequestBuilder
from anonymiser.server_interface import ServerInterface
from threading import Thread

__author__ = 'johannes'


class Processor(Thread):
    """
    This class is a container for a request-parser, a request-builder and a server-interface. A new instance of this
    class is spawned by the client-interface for each unique client.
    """

    def __init__(self, client_interface, address, conn_socket):
        Thread.__init__(self)
        self.client_interface = client_interface
        self.address = address
        self.conn_socket = conn_socket
        self.request_parser = RequestParser()
        self.request_builder = RequestBuilder()
        self.server_interface = ServerInterface()

    def run(self):
        """
        Gets called when a new instance of this class (processor) is created. Checks if there already is a processor-
        instance for this client and shuts down if so. Also calls the request-parser, the request-builder and the
        server-interface. Then proceeds by sending the data it received from the server-interface to the client.
        """

        reg_status = self.client_interface.register(self.address)

        if reg_status == -1:
            return -1

        parser_output, host, is_ssl = self.request_parser.start(self.conn_socket)
        if parser_output == -1 or parser_output is None:
            return -1
        builder_output = self.request_builder.start(parser_output, is_ssl)
        website = self.server_interface.send_data(builder_output, host, is_ssl)
        # Send data to client (browser)
        if website != -1:
            print('Sending data to client: ')
            print(website)
            self.conn_socket.sendall(website)
        else:
            print('Server interface returned -1, couldn\'t retrieve website')

    def stop(self):
        # TODO Improve stopping processor threads.
        """
        De-registers a thread in client-interface-class
        """

        self.client_interface.deregister(self.address)
