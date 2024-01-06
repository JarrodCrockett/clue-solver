import tkinter as tk
from tkinter import simpledialog
from CluePuzzleSolver import ClueSolver

class ClueSolverGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Clue Solver")
        self.geometry("400x300")
        self.cluesolver = ClueSolver()
        self.create_widgets()

    def create_widgets(self):
        # Add your GUI components here
        label = tk.Label(self, text="Clue Solver GUI")
        label.pack(pady=10)

        button_players_item = tk.Button(self, text="Players", command=self.players_button_click, padx=10, pady=10)
        button_players_item.pack(pady=10)

        button_get_best_guess = tk.Button(self, text="Get Best Guess", command=self.get_best_guess_button_click, padx=10, pady=10)
        #button_get_best_guess.pack()

        button_print_ptables = tk.Button(self, text="Print P Table", command=self.print_ptable_button_click, padx=10, pady=10)
        button_print_ptables.pack(pady=10)


    def players_button_click(self):
        self.create_player_buttons("Player Selection")

    def showed_item_button_click(self, player):
        items = self.cluesolver.get_unknown_characters() + self.cluesolver.get_unknown_rooms() + self.cluesolver.get_unknown_weapons()
        self.create_item_buttons("Showed Item",player, items, 1)

    def heard_guess_button_click(self, player):
        guess = self.choose_items_from_list('Enter the guess you heard', self.cluesolver.get_all_characters() + self.cluesolver.get_all_rooms() + self.cluesolver.get_all_weapons(), 4)
        if guess:
            self.cluesolver.make_guess(player, guess)

    def create_player_buttons(self, title, num_items=None):
        # Create a new Toplevel window
        new_window = tk.Toplevel(self)
        new_window.geometry("300x400")
        new_window.title(title)
        players = self.cluesolver.get_players()
        for player in players:
            button = tk.Button(new_window, text=player, command=lambda player=player: self.create_player_menu(f"{player} menu", player, new_window), padx=10, pady=5)
            button.pack(pady=10)

    def change_player_name(self, title, player):
        new_name = simpledialog.askstring(title, f"Type the new player name.", parent=self)
        self.cluesolver.rename_player(player, new_name)

    def create_player_menu(self, title, player, new_window):
        new_window = tk.Toplevel(self)
        new_window.geometry("300x400")
        new_window.title(title)
        button_change_player_name = tk.Button(new_window, text="Change Name", command=lambda player=player: self.change_player_name_button_click(title, player, new_window), padx=10, pady=10)
        button_change_player_name.pack(pady=10)

        button_saw_item = tk.Button(new_window, text="Saw Card", command=lambda player=player: self.showed_item_button_click(player), padx=10, pady=10)
        button_saw_item.pack(pady=10)

        button_heard_guess = tk.Button(new_window, text="Heard Player Guess", command=lambda player=player: self.heard_guess_button_click(player), padx=10, pady=10)
        button_heard_guess.pack(pady=10)

        button_shown_known_cards = tk.Button(new_window, text="Show Known Cards", command=lambda player=player: self.print_known_cards_button_click(player), padx=10, pady=10)
        button_shown_known_cards.pack(pady=10)

        button_shown_guesses_ = tk.Button(new_window, text="Show Guesses", command=lambda player=player: self.print_player_guesses_button_click(player), padx=10, pady=10)
        button_shown_guesses_.pack(pady=10)

        return None

    def change_player_name_button_click(self, title, player, new_window):
        self.change_player_name(title, player)

    def create_item_buttons(self, title, player, items, num_items=None):
        # Create a new Toplevel window
        new_window = tk.Toplevel(self)
        new_window.geometry("300x600")
        new_window.title(title)
        
        for item in items:
            button = tk.Button(new_window, text=item, command=lambda player=player, item=item: self.saw_player_card(player, item))
            button.pack()

    def saw_player_card(self, player, item):
        self.cluesolver.saw_card(player, item)

    def print_known_cards_button_click(self, player):
        self.cluesolver.show_player_known_cards(player)

    def print_player_guesses_button_click(self, player):
        self.cluesolver.show_player_guess_list(player)

    def handle_dynamic_button_click(self, title, player, item, num_items=None, window=None):
        if num_items:
            selected_items = self.choose_items_from_list(title, [item], num_items)
            if selected_items:
                print(f"{title}: {', '.join(selected_items)}")
                # Perform the desired action with the selected items (e.g., self.clue_solver.heard_item)
        else:
            print(player)
            print(f"{title}: {item}")
            self.cluesolver.saw_card(player, item)
            # Perform the desired action with the selected item (e.g., self.clue_solver.saw_item)

        # Close the new window after handling the click
        if window:
            window.destroy()

    def print_ptable_button_click(self):
        self.cluesolver.show_probability_table()


    def choose_item_from_list(self, title, items):
        item = simpledialog.askstring(title, "Choose an item:", initialvalue=items[0], parent=self)
        if item and item in items:
            return item
        return None

    def choose_items_from_list(self, title, items, num_items):
        items.append('true')
        items.append('false')
        items_str = simpledialog.askstring(title, f'List 3 items and if they showed a card "True" or "False"(separated by commas):', parent=self)
        if items_str:
            selected_items = items_str.split(',')
            print(selected_items)
            print(items)
            selected_items = [item.strip() for item in selected_items if item.strip() in items]
            if len(selected_items) == num_items:
                print(selected_items)
                return selected_items
        return None

    def get_best_guess_button_click(self):
        self.cluesolver.get_best_guess()


def main():
    app = ClueSolverGUI()
    app.mainloop()

if __name__ == "__main__":
    main()