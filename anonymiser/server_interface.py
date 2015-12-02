import socket
import re

__author__ = 'johannes'


class ServerInterface:
    """
    This class is responsible for any communication with a webserver over the internet: Sending requests it gets from
    the request-builder and receiving HTTP-responses it gets from the webserver. It automatically passes the data to
    the client.
    """

    def send_data(self, request, server):
        """
        Gets called by processor-class, calls send-request-method which actually sends the request to the
        web-server.
        """

        return self.send_request(request, server)

    def send_request(self, request, server):
        """
        Opens a connection to the web-server, sends the request and waits for a response. It then proceeds by forwarding
        the data received to the processor-class.
        """

        print('[I] Sending data to client')

        web_serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        web_serv_socket.connect((server, 80))
        web_serv_socket.sendall(request)

        # TODO Adjust chunk-size (1 byte at the moment)
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
        else:
            data = -1

        return data
