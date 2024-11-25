import sys
from game import AchtungDieKurveGame

game = AchtungDieKurveGame(mode="headless")

modulename = 'pygame'
if modulename in sys.modules:
    print(f"{modulename} was imported!")
else:
    print(f'{modulename} was NOT imported')