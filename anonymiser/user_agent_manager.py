import random

__author__ = 'jpawelczyk'


class UserAgentManager:
    """
    Diese Klasse stellt zufällige User-Agent-Strings zur Verfügung.
    """

    def __init__(self):
        # Pfad zur Datei, die die User-Agent-Strings enthält.
        self.ua_string_file_path = '/home/johannes/Dokumente/Anonymizer/ua_strings.txt'

        self.ua_string_count = 0
        ua_file = open(self.ua_string_file_path, 'r')
        self.ua_list = []
        for ua_string in ua_file:
            self.ua_string_count += 1
            self.ua_list.append(ua_string)
        ua_file.close()

    def get_ua_string(self):
        """
        Diese Methode gibt einen zufälligen User-Agent-String zurück.
        """

        i = random.choice(range(self.ua_string_count))

        return self.ua_list[i]
