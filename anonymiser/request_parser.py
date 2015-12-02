__author__ = 'johannes'


class RequestParser:
    """
    This class is responsible for receiving and parsing HTTP-requests from a client (browser).
    It returns a dictionary containing the information extracted from the HTTP-request.
    """

    def __init__(self):
        self.host = ''

    def start(self, conn_socket):
        """
        Calls receive_data()-method and forwards data it returns to caller
        """

        return self.parse_data(conn_socket), self.host

    def receive_data(self, conn_socket):
        """
        This method receives the data from the client (browser).
        """

        print('[I] Retrieving data from client')

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

        return data

    def parse_data(self, conn_socket):
        """
        This method actually parses a request. It should receive a list of byte-strings. Returns a dictionary
        containing all the parsed data from the data it received.
        """

        print('[I] Parsing data')

        # Call receive_data() function to get raw_data from client
        raw_data = self.receive_data(conn_socket)

        try:
            data_list = []
            for raw_string in raw_data:
                # Decode byte-data to human-readable data
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
