import tkinter as tk
from tkinter import simpledialog
from CluePuzzleSolver import Player, ProbabilityTable

class ClueSolverGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Clue Solver")
        self.geometry("400x300")

        self.characters = ["mustard", "scarlett", "plum", "peacock", "green","orchid"]
        self.weapons = ["candlestick", "dagger", "pipe", "revolver", "rope", "wrench"]
        self.rooms = ["kitchen", "ballroom", "conservatory", "dining", "billiard", "library", "lounge", "hall", "study"]
        self.players = ['computer', 'player2', 'player3', 'player4']

        self.p_table = ProbabilityTable(self.characters, self.rooms, self.weapons)

        self.create_widgets()

    def create_widgets(self):
        # Add your GUI components here
        label = tk.Label(self, text="Clue Solver")
        label.pack(pady=10)
        for player_name in self.players:
            button = tk.Button(self, text=player_name, command=lambda p=player_name: self.open_player_window(p))
            button.pack()

        button_print_ptables = tk.Button(self, text="Print P Table", command=self.print_ptable_button_click)
        button_print_ptables.pack()

    def create_player(self, player_name):
        # Create a player for the given name
        player = Player(player_name)
        # Optionally, you can store the player object or do something with it
        print(f"Player {player_name} created with known cards: {player.has_cards}")

    def open_player_window(self, player_name):
        # Create a new top-level window for the player
        player_window = tk.Toplevel(self)
        player_window.title(f"{player_name}'s Functions")

        # Create buttons for player functions
        for method_name in dir(Player):
            if callable(getattr(Player, method_name)) and not method_name.startswith("__"):
                button = tk.Button(player_window, text=method_name, command=lambda m=method_name: self.call_player_function(player_name, m))
                button.pack()

    def call_player_function(self, player_name, function_name):
        # Call the selected function from the Player class
        player = Player(player_name)
        function = getattr(player, function_name)
        function()

    def saw_item_button_click(self):
        self.create_item_buttons("Saw Item", self.rooms + self.characters + self.weapons)

    def heard_item_button_click(self):
        items = self.choose_items_from_list("List 3 items (room, char, wep)", self.rooms + self.characters + self.weapons, 3)
        if items:
            room, character, weapon = items
            print(f"Heard Item: {room}, {character}, {weapon}")
            self.clue_solver.heard_item(room, character, weapon)

    def create_item_buttons(self, title, items, num_items=None):
        # Create a new Toplevel window
        new_window = tk.Toplevel(self)
        new_window.title(title)

        for item in items:
            button = tk.Button(new_window, text=item, command=lambda item=item: self.handle_dynamic_button_click(title, item, num_items, new_window))
            button.pack()

    def handle_dynamic_button_click(self, title, item, num_items=None, window=None):
        if num_items:
            selected_items = self.choose_items_from_list(title, [item], num_items)
            if selected_items:
                print(f"{title}: {', '.join(selected_items)}")
                # Perform the desired action with the selected items (e.g., self.clue_solver.heard_item)
        else:
            print(f"{title}: {item}")
            self.clue_solver.saw_item(item)
            # Perform the desired action with the selected item (e.g., self.clue_solver.saw_item)

        # Close the new window after handling the click
        if window:
            window.destroy()

    def print_ptable_button_click(self):
        self.p_table.show_probability_table()

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