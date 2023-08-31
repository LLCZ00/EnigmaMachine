#!/usr/bin/python3
"""
Enigma Machine Tests
"""


import unittest
from enigmamachine import EnigmaMachine


class TestEnigma(unittest.TestCase):

	def test_encrypt(self):
		enigma = EnigmaMachine()
		enigma.setRotorTypes(4, 2, 5)
		enigma.setRotorRings(15, 23, 26)
		enigma.setRotorPositions('A', 'B', 'C')
		enigma.setPlugboard("LZ SQ AG")
		self.assertEqual(enigma("message"), "ZDFXEFA")

	def test_decrypt(self):
		enigma = EnigmaMachine()
		enigma.setRotorTypes(4, 2, 5)
		enigma.setRotorRings(15, 23, 26)
		enigma.setRotorPositions('A', 'B', 'C')
		enigma.setPlugboard("LZ SQ AG")
		self.assertEqual(enigma("ZDFXEFA"), "MESSAGE")



if __name__ == "__main__":
	unittest.main()
