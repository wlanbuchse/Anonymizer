from anonymiser.user_agent_manager import UserAgentManager

__author__ = 'johannes'


class RequestBuilder:
    """
    Diese Klasse ist dafür verantwortlich eine gültige HTTP-Request zu erzeugen, basierend auf den Daten, die sie vom
    Request-Parser erhält. Sie gibt erzeugte Requests automatisch an das Server-Interface weiter.
    """

    def __init__(self):
        pass

    def start(self, parser_output):
        """
        Diese Methode wird von der Processor-Klasse aufgerufen. Ruft wiederum die build_request()-Methode auf, die die
        Request tatsächlich erzeugt.
        """

        return self.build_request(parser_output)

    def build_request(self, parser_output):
        """
        Wandelt das Dictionary, das sie vom Request-Parser erhält in eine gültige Request in Form eines Byte-Strings um.
        """

        print('[I] Erzeuge Request')

        # Hole einen zufälligen User-Agent-String vom User-Agent-Manager
        manager = UserAgentManager()
        ua_string = "User-Agent: " + manager.get_ua_string()

        # Initialisiere die Request mit den obligatorischen Zeilen.
        values_list = [
            parser_output['request'],
            parser_output['host'],
            ua_string,
            parser_output['accept'],
            parser_output['accept-language'],
            parser_output['accept-encoding']
        ]

        # Nicht-obligatorische Zeilen
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

        return bytes(data, 'utf-8')
