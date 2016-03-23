from anonymiser.client_interface import ClientInterface

__author__ = 'johannes'


"""
Dieses Skript wird verwendet um das Programm zu starten.
"""

# Gib einige allgemeine Inforamtionen aus.
print('Willkommen!')
print('Dieses Programm verschleiert Ihren User-Agent-String um Ihre Privatsphäre zu schützen.')
print('\n')
print('[E] -> Fehler')
print('[W] -> Warnung')
print('[I] -> Hinweis')
print('\n\n')

intf = ClientInterface()
intf.start()
