# from CluePuzzleSolver import ClueSolver, TruthTable

# def main():
#     characters = ["Colonel Mustard", "Miss Scarlett", "Professor Plum", "Mrs. Peacock", "Mr. Green", "Mrs. White"]
#     weapons = ["Candlestick", "Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"]
#     rooms = ["Kitchen", "Ballroom", "Conservatory", "Dining Room", "Billiard Room", "Library", "Lounge", "Hall", "Study"]

#     # Assume some objects are entered initially

#     clue_solver = ClueSolver(rooms, characters, weapons)
#     truth_table = TruthTable(rooms, characters, weapons)
#     clue_solver.saw_item("Library")
#     clue_solver.saw_item("Study")
#     clue_solver.heard_item("Kitchen", "Colonel Mustard", "Candlestick")
#     clue_solver.print_probability_tables()

# if __name__ == "__main__":
#     main()

import tkinter as tk
from tkinter import simpledialog
from CluePuzzleSolver import ClueSolver, TruthTable

class ClueSolverGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Clue Solver")
        self.geometry("400x300")

        self.characters = ["Colonel Mustard", "Miss Scarlett", "Professor Plum", "Mrs. Peacock", "Mr. Green", "Mrs. White"]
        self.weapons = ["Candlestick", "Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"]
        self.rooms = ["Kitchen", "Ballroom", "Conservatory", "Dining Room", "Billiard Room", "Library", "Lounge", "Hall", "Study"]

        self.clue_solver = ClueSolver(self.rooms, self.characters, self.weapons)
        self.truth_table = TruthTable(self.rooms, self.characters, self.weapons)

        self.create_widgets()

    def create_widgets(self):
        # Add your GUI components here
        label = tk.Label(self, text="Clue Solver GUI")
        label.pack(pady=10)

        button_saw_item = tk.Button(self, text="Saw Item", command=self.saw_item_button_click)
        button_saw_item.pack()

        button_heard_item = tk.Button(self, text="Heard Item", command=self.heard_item_button_click)
        button_heard_item.pack()

        button_print_ptables = tk.Button(self, text="Print P Table", command=self.print_ptable_button_click)
        button_print_ptables.pack()

        button_print_Ttables = tk.Button(self, text="Print T Table", command=self.print_truthtable_button_click)
        button_print_Ttables.pack()

    def saw_item_button_click(self):
        item = self.choose_item_from_list("Choose an item", self.rooms + self.characters + self.weapons)
        if item:
            print(f"Saw Item: {item}")
            self.clue_solver.saw_item(item)

    def heard_item_button_click(self):
        items = self.choose_items_from_list("List 3 items (room, char, wep)", self.rooms + self.characters + self.weapons, 3)
        if items:
            room, character, weapon = items
            print(f"Heard Item: {room}, {character}, {weapon}")
            self.clue_solver.heard_item(room, character, weapon)

    def print_ptable_button_click(self):
        self.clue_solver.print_probability_tables()

    def print_truthtable_button_click(self):
        self.clue_solver.print_truth_table()

    def choose_item_from_list(self, title, items):
        item = simpledialog.askstring(title, "Choose an item:", initialvalue=items[0], parent=self)
        if item and item in items:
            return item
        return None

    def choose_items_from_list(self, title, items, num_items):
        items_str = simpledialog.askstring(title, f"Choose {num_items} items (separated by commas):", parent=self)
        if items_str:
            selected_items = items_str.split(',')
            selected_items = [item.strip() for item in selected_items if item.strip() in items]
            if len(selected_items) == num_items:
                return selected_items
        return None


def main():
    app = ClueSolverGUI()
    app.mainloop()

if __name__ == "__main__":
    main()