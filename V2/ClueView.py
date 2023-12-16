import tkinter as tk
from tkinter import simpledialog
from CluePuzzleSolver import Player, ProbabilityTable


characters = ["mustard", "scarlett", "plum", "peacock", "green","orchid"]
weapons = ["candlestick", "dagger", "pipe", "revolver", "rope", "wrench"]
rooms = ["kitchen", "ballroom", "conservatory", "dining", "billiard", "library", "lounge", "hall", "study"]

p_table = ProbabilityTable(characters, rooms, weapons)
p_table.show_probability_table()
player = Player('player1')

player.make_guess(('green', 'study', 'dagger', True))
p_table.guess_update(('green', 'study', 'dagger', True))
p_table.guess_update(('green', 'hall', 'dagger', True))
p_table.guess_update(('green', 'library', 'rope', True))
p_table.guess_update(('green', 'dining', 'pipe', True))
print()
p_table.show_probability_table()