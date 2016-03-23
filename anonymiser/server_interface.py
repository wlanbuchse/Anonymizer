import socket
import re

__author__ = 'johannes'


class ServerInterface:
    """
    Diese Klasse ist für die Kommunikation mit einem Webserver zuständig: Sendet Daten vom Request-Builder und empfängt
    Daten vom Webserver. Leitet die Daten automatisch weiter.
    """

    def send_data(self, request, server):
        """
        Wird vom Processor aufgerufen, ruft wiederum send_request()-Methode auf, die die Request tatsächlich sendet.
        """

        return self.send_request(request, server)

    def send_request(self, request, server):
        """
        Stellt eine Verbindung zum Webserver her, sendet die Request und wartet auf eine Antwort. Leitet dann die
        empfangenen Daten an den Processor weiter.
        """

        print('[I] Sende Daten zum Webserver')

        web_serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        web_serv_socket.connect((server, 80))
        web_serv_socket.sendall(request)

        data = b''
        newl_count = 0
        while True:
            chunk = web_serv_socket.recv(1)

            if not chunk:
                break
            data += chunk
            if chunk == b'\n':
                newl_count += 1
                if newl_count >= 2:
                    break
            elif (chunk != b'\n') and (chunk != b'\r'):
                newl_count = 0

        data = b''
        newl_count = 0
        while True:
            chunk = web_serv_socket.recv(1)

            if not chunk:
                break
            data += chunk
            if chunk == b'\n':
                newl_count += 1
                if newl_count >= 2:
                    break
            elif (chunk != b'\n') and (chunk != b'\r'):
                newl_count = 0

        web_serv_socket.close()

        match = re.search('<html.*</html>', str(data))
        if match:
            data = bytes(match.group(0), 'utf-8')

        return data
