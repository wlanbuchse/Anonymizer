from anonymiser.request_parser import RequestParser
from anonymiser.request_builder import RequestBuilder
from anonymiser.server_interface import ServerInterface
from threading import Thread

__author__ = 'johannes'


class Processor(Thread):
    """
    Diese Klasse ist ein Container für einen Request-Parser, einen Request-Builder und ein Server-Interface.
    Das Client-Interface erstellt eine neue Instanz dieser Klasse für jeden einzigartigen Client.
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
        Diese Methode wird ausgeführt sobald eine neue Instanz dieser Klasse erstellt wird. Sie überprüft, ob schon eine
        andere Processor-Instanz den selben Client behandelt und terminiert wenn das der Fall ist. Ruft außerdem
        Request-Parser, Request-Builder und Server-Interface auf. Sendet dann die vom Server-Interface erhaltenen Daten
        zurück an den Client (den Webbrowser).
        """

        print('[I] Neuer Thread erstellt um mit diesem Client zu kommunizieren.')

        reg_status = self.client_interface.register(self.address)

        if reg_status == -1:
            print('[I] Eine andere Processor-Instanz behandelt schon diesen Client, terminiere.')
            return -1

        parser_output, host = self.request_parser.start(self.conn_socket)
        if parser_output == -1 or parser_output is None:
            print('[E] Parser returned -1')
        builder_output = self.request_builder.start(parser_output)
        website = self.server_interface.send_data(builder_output, host)

        # Sende Daten zurück zum Client (Webbrowser)
        if website != -1:
            self.conn_socket.sendall(website)
        else:
            print('[E] Server-Interface hat -1 zurückgegeben, konnte Webseite nicht holen.')

    def stop(self):
        self.client_interface.deregister(self.address)
