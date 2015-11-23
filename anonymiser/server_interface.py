import socket
import re

__author__ = 'johannes'


class ServerInterface:
    """
    This class in responsible for any communication with a webserver over the internet: Sending requests it gets from
    the request-builder and receiving HTTP-responses it gets from said webserver. It automatically passes the data to
    the client over passed-through socket.
    """

    def __init__(self):
        pass

    def send_data(self, request, server, is_ssl):
        """
        Gets called by processor-class, calls send-request-method which actually sends the request to the
        web-server, or the send-ssl-request-method if is-ssl-flag is set to true.
        """

        return self.send_ssl_request(request, server) if is_ssl else self.send_request(request, server)

    def send_request(self, request, server):
        """
        Opens a connection to the web-server, sends the request and waits for a response. It then proceeds by forwarding
        the data received to the processor-class. Only works on non-ssl-requests. There is a separate method for sending
        ssl-requests.
        """

        print('Sending non-SSL-request to server:')
        print(request)
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

        # TODO Only if connection-type is not keep-alive?
        web_serv_socket.close()

        match = re.search('<html.*</html>', str(data))
        if match:
            data = bytes(match.group(0), 'utf-8')
        else:
            data = -1

        return data

    def send_ssl_request(self, request, server):
        """
        Opens a connection to the web-server, sends the request and waits for a response. It then proceeds by forwarding
        the data received to the processor-class. Only works on ssl-requests. There is a separate method for sending
        non-ssl-requests.
        """

        print('Sending SSL-request to server:')
        print(request)
        web_serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        web_serv_socket.connect((server, 443))
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

        # TODO Only if connection-type is not keep-alive?
        web_serv_socket.close()

        match = re.search('<html.*</html>', str(data))
        if match:
            data = bytes(match.group(0), 'utf-8')
        else:
            data = -1

        return data
