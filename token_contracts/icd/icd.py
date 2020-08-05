from iconservice import *
from .tokens.IRC2mintable import IRC2Mintable
from .tokens.IRC2burnable import IRC2Burnable

TAG = 'ICD'

TOKEN_NAME = 'ICONDollar'
SYMBOL_NAME = 'ICD'
INITIAL_SUPPLY = 0
DECIMALS = 18

class ICONDollar(IRC2Mintable, IRC2Burnable):

	def on_install(self) -> None:
		super().on_install(TOKEN_NAME, SYMBOL_NAME, INITIAL_SUPPLY, DECIMALS)
