import socket
from anonymiser.processor import Processor
from anonymiser.user_agent_manager import UserAgentManager

__author__ = 'johannes'


class ClientInterface:
    """
    Diese Klasse ist für den Empfang von Daten vom Client (dem Webbrowser) zuständig. Sie erstellt eine Neue Instanz der
    Processor-Klasse für jeden einzigartigen Client.
    """

    def __init__(self):
        # Das Programm verwendet Port 8008 auf localhost um auf Anfragen von einem Client (Webbrowser) zu warten.
        self.address = ('localhost', 8008)
        # Diese Liste führt Buch über alle aktiven Processor-Instanzen um zu gewährleisten, dass für keinen Client zwei
        # Processor-Instanzen existieren. Sie wird von den register()- und deregister()-Methoden verwendet.
        self.proc_register = []
        self.listener_running = False
        self.user_agent_manager = UserAgentManager()

    def start(self):
        """
        Startet den Listener auf Port 8008 auf localhost, wie im Konstruktor festgelegt (s.o.).
        """

        self.start_listener()

    def start_listener(self):
        """
        Das Programm fängt an auf Anfragen zu warten. Akzeptiert Verbindungen in einer Schleife und erstellt für jeden
        einzigartigen Client eine Processor-Instanz.
        """

        # Erstelle den Socket
        self.listener_running = True
        listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener_socket.bind(self.address)
        listener_socket.listen(1)

        print('[I] Warte auf Verbindungen auf Port ' + str(self.address[1]))

        while self.listener_running:
            connection, address = listener_socket.accept()
            # Starte eine neue Processor-Instanz in einem neuen Thread für diesen Client.
            # Sollte schon ein Processor existieren, der sich mit dem selben Client beschäftigt, dann terminiert sich
            # die neue Processor-Instanz selber.
            thread = Processor(self, address, connection)
            thread.start()

    def register(self, address):
        """
        Diese Methode wird von Processor-Instanzen verwendet um zu prüfen, ob schon eine andere Processor-Instanz mit
        dem selben Client kommuniziert um zu vermeiden, dass Redundanzen entstehen. Verwendet die proc_register-Variable.
        """

        if address in self.proc_register:
            # Dies lässt den Aufrufer wissen, dass schon eine Processor-Instanz exisitiert, die den selben Client
            # versorgt.
            return -1
        else:
            self.proc_register.append(address)
            return 1

    def deregister(self, address):
        """
        Diese Methode lässt das client_interface wissen, dass die aufrufende Processor-Instanz terminiert und ggf. eine
        neue Instanz für ihren Client erstellt werden darf.
        """

        if address not in self.proc_register:
            return -1
        else:
            self.proc_register.remove(address)
            return 1
