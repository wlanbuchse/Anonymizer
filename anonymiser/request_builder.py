from anonymiser.user_agent_manager import UserAgentManager

__author__ = 'johannes'


class RequestBuilder:
    """
    This class is responsible for building correct HTTP-requests without any sensible information based on the
    information it gets from the request-parser. It automatically passes requests to the server-interface to process.
    """

    def __init__(self):
        pass

    def start(self, parser_output, is_ssl):
        """
        Gets called by the processor-class. Calls build-request-method which actually builds
        the request or build-ssl-request-method if is-ssl-flag is set to true.
        """

        return self.build_ssl_request(parser_output) if is_ssl else self.build_request(parser_output)

    def build_request(self, parser_output):
        """
        Assembles the dictionary it gets from the request-parser-class into a byte-string
        in the appropriate order to send to the web-server. Only works on non-ssl-data. There is
        a separate method for building ssl requests.
        """

        # Get random User-Agent-String from user_agent_manager-class
        manager = UserAgentManager()
        ua_string = "User-Agent: " + manager.get_ua_string()

        # Initialise with obligatory items (see comment in request_parser-class)
        values_list = [
            parser_output['request'],
            parser_output['host'],
            ua_string,
            parser_output['accept'],
            parser_output['accept-language'],
            parser_output['accept-encoding']
        ]

        # Non-obligatory items
        if 'dnt' in parser_output.keys():
            values_list.append(parser_output['dnt'])
        if 'cookie' in parser_output.keys():
            values_list.append(parser_output['cookie'])
        if 'connection' in parser_output.keys():
            values_list.append(parser_output['connection'])

        data = '\r\n'.join(values_list)
        data = data.rstrip('\r\n')
        data = data.lstrip('\r\n')
        data += '\r\n\r\n'

        print('The request-builder returns following data:')
        print(data)

        return bytes(data, 'utf-8')

    def build_ssl_request(self, parser_output):
        """
        Assembles the dictionary it gets from the request-parser-class into a byte-string
        in the appropriate order to send to the web-server. Only works on ssl-data. There is
        a separate method for building non-ssl requests.
        """

        # TODO - Continue here -
        #
        # Request built based on data in SSL-request looks fine but
        # the server interface returns -1 ...

        # Get random User-Agent-String from user_agent_manager-class
        manager = UserAgentManager()
        ua_string = 'User-Agent: ' + manager.get_ua_string().rstrip('\n')

        # Initialise with obligatory items (see comment in request_parser-class)
        values_list = [
            'GET ' + parser_output['host'] + ' HTTP/1.1',
            'Host: ' + parser_output['host'],
            ua_string
        ]

        # TODO Add other possible options (s.a.)
        if 'connection' in parser_output.keys():
            values_list.append(parser_output['connection'])

        data = '\r\n'.join(values_list)
        data = data.rstrip('\r\n')
        data = data.lstrip('\r\n')
        data += '\r\n\r\n'

        print('(SSL) Request-builder returns following data: ')
        print(data)

        return bytes(data, 'utf-8')
