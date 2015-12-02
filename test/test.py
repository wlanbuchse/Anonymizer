from anonymiser.client_interface import ClientInterface

__author__ = 'johannes'


"""
This script is used to test the program.
"""

# Print some general information
print('Welcome to Anonymizer!')
print('This program will randomize your User-Agent-String to protect your privacy.')
print('\n')
print('[E] -> Error')
print('[W] -> Warning')
print('[I] -> Information')
print('\n\n')

intf = ClientInterface()
intf.start()
