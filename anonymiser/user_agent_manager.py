import random

__author__ = 'jpawelczyk'


class UserAgentManager:
    """
    Other classes get their random User-Agent-Strings from this classes' get_ua_string()-method.
    """

    def __init__(self):
        # Path to the file containing the UAS that should be used
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
        This method returns a random User-Agent-String.
        """

        i = random.choice(range(self.ua_string_count))

        return self.ua_list[i]
