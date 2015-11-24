__author__ = 'johannes'


class RequestParser:
    """
    This class is responsible for receiving and parsing incoming HTTP-requests from a client (browser).
    An instance automatically passes received and parsed requests to the appropriate request-builder.
    """

    def __init__(self):
        self.host = ''
        self.is_ssl = False

    def start(self, conn_socket):
        """
        Calls receive_data()-method and forwards data it returns to caller
        """

        # TODO start() should call parse_data() which calls receive_data()
        return self.receive_data(conn_socket), self.host, self.is_ssl

    def receive_data(self, conn_socket):
        """
        This method gets the data from the client (browser) and calls parse_data()-method
        """

        data = []
        # This variable is required to be able to see where a request ends (requests are terminated by two
        # trailing \r\n's)
        newl_count = 0
        while True:
            # TODO Adjust chunk-size (1 byte at the moment)
            chunk = conn_socket.recv(1)
            # If receives nothing, move on to parsing
            if not chunk:
                break

            # This code breaks out of the loop when request ends (s.a.) by counting occurrences of '\n'
            if chunk == b'\n':
                newl_count += 1
                if newl_count >= 2:
                    break
            elif chunk != b'\n' and chunk != b'\r':
                newl_count = 0

            data.append(chunk)

        print('Received following request from client: ')
        print(b''.join(data).decode('utf-8'))

        # Check if it's SSL-data
        data_as_string = b''.join(data).decode('utf-8')
        first_word = data_as_string[:data_as_string.find(' ')].lower()

        if 'connect' in first_word:
            self.is_ssl = True
            return self.parse_ssl_data(data)
        else:
            self.is_ssl = False
            return self.parse_data(data)

    def parse_data(self, raw_data):
        """
        This method actually parses a request. It should receive a list of byte-strings. Returns a dictionary
        containing all the parsed data from the data it received. Only works on non-SSL requests. There
        is a separate method for parsing SSL requests.
        """

        try:
            data_list = []
            for raw_string in raw_data:
                # Decode byte-data to actual human-readable data
                data_list.append(raw_string.decode('utf-8'))
            data_string = ''.join(data_list)
            data_list = data_string.split('\r\n')

            # Declare and initialise output-dictionary with obligatory items
            output_dict = {
                'request': data_list[0],
                'host': data_list[1],
                'user-agent': data_list[2],
                'accept': data_list[3],
                'accept-language': data_list[4],
                'accept-encoding': data_list[5]
            }

            # Add non-obligatory items if present, not every request contains these
            if len(data_list) >= 6:
                # Don't check obligatory items
                for e in data_list[6:]:
                    if 'dnt' in e.lower():
                        output_dict['dnt'] = e
                    if 'cookie' in e.lower():
                        output_dict['cookie'] = e
                    if 'connection' in e.lower():
                        output_dict['connection'] = e

            # Grab host-entry (aka. the address of the webserver to connect to)
            host_entry = output_dict['host']
            host_entry = host_entry[host_entry.find(':') + 2:]
            self.host = host_entry

            return output_dict
        except UnicodeDecodeError:
            return -1

    def parse_ssl_data(self, raw_data):
        """
        This method actually parses a request. It should receive a list of byte-strings. Returns a dictionary
        containing all the parsed data from the data it received. Only works on SSL requests. There
        is a separate method for parsing non-SSL requests.
        """

        try:
            data_list = []
            for raw_string in raw_data:
                # Decode byte-data to actual human-readable data
                data_list.append(raw_string.decode('utf-8'))
            data_string = ''.join(data_list)
            data_list = data_string.split('\r\n')

            output_dict = {
                'connection': data_list[3],
                'host': data_list[4]
            }

            host_port_string = output_dict['host']
            host_port_list = host_port_string.split(':')
            _host = host_port_list[1].lstrip(' ')
            _port = host_port_list[2]

            output_dict['host'] = _host

            print('Host: ' + _host)
            print('Port: ' + _port)

            self.host = _host

            return output_dict
        except UnicodeDecodeError:
            return -1
