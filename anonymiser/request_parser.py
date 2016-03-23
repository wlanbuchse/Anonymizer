__author__ = 'johannes'


class RequestParser:
    """
    Diese Klasse ist dafür verantwortlich, Anfragen vom Client (Webbrowser) zu empfangen und diese zu parsen.
    Gibt ein Dictionary mit den extrahierten/geparsten Informationen zurück.
    """

    def __init__(self):
        self.host = ''

    def start(self, conn_socket):
        """
        Ruft parse_data()-Methode auf und leitet zurückgegebene Daten an Aufrufer weiter.
        """

        return self.parse_data(conn_socket), self.host

    def receive_data(self, conn_socket):
        """
        Diese Methode empfängt die Daten vom Client.
        """

        print('[I] Empfange Daten vom Client')

        data = []
        # Diese Variable ist nötig um das Ende einer Request zu finden (Requests enden mit den Zeichen '\r\n\r\n').
        newl_count = 0
        while True:
            chunk = conn_socket.recv(1)
            # Wenn nichts empfangen wird, weiter mit parsen
            if not chunk:
                break

            # Dieser Code verlässt die Schleife wenn die Request endet (s.o.).
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
        Diese Methode parst die Request tatsächlich. Sie sollte eine Liste von Byte-Strings erhalten. Gibt ein
        Dictionary mit den geparsten Informationen zurück.
        """

        print('[I] Parse Request')

        # Rufe receive_data()-Methode auf um Daten vom Client zu erhalten.
        raw_data = self.receive_data(conn_socket)

        try:
            data_list = []
            for raw_string in raw_data:
                # Dekodiere Byte-Strings
                data_list.append(raw_string.decode('utf-8'))
            data_string = ''.join(data_list)
            data_list = data_string.split('\r\n')

            # Deklariere und initialisiere Dictionary mit obligatorischen Zeilen.
            output_dict = {
                'request': data_list[0],
                'host': data_list[1],
                'user-agent': data_list[2],
                'accept': data_list[3],
                'accept-language': data_list[4],
                'accept-encoding': data_list[5]
            }

            # Füge nicht-obligatorische Zeilen hinzu, falls vorhanden. Nicht jede Request enthält diese Zeilen.
            if len(data_list) >= 6:
                for e in data_list[6:]:
                    if 'dnt' in e.lower():
                        output_dict['dnt'] = e
                    if 'cookie' in e.lower():
                        output_dict['cookie'] = e
                    if 'connection' in e.lower():
                        output_dict['connection'] = e

            # Extrahiere host-entry, d.h. die Adresse des Ziel-Servers
            host_entry = output_dict['host']
            host_entry = host_entry[host_entry.find(':') + 2:]
            self.host = host_entry

            return output_dict
        except UnicodeDecodeError:
            return -1
