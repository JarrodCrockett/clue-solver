import tkinter as tk
from tkinter import simpledialog
from CluePuzzleSolver import ClueSolver

class ClueSolverGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Clue Solver")
        self.geometry("400x500")
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

        button_print_all_known_cards = tk.Button(self, text="Print All Known Cards", command=self.print_all_known_cards_button_click, padx=10, pady=10)
        button_print_all_known_cards.pack(pady=10)

        button_clr_console = tk.Button(self, text="Clear Console", command=self.clr_console_button_click, padx=10, pady=10)
        button_clr_console.pack(pady=10)


    def print_all_known_cards_button_click(self):
        self.cluesolver.get_all_known_cards()

    def players_button_click(self):
        self.create_player_buttons("Player Selection")

    def showed_item_button_click(self, player):
        items = self.cluesolver.get_all_characters() + self.cluesolver.get_all_rooms() + self.cluesolver.get_all_weapons()
        self.create_item_buttons("Showed Item",player, items, 1)

    def heard_guess_button_click(self, player):
        guess = self.choose_items_from_list('Enter the guess you heard', self.cluesolver.get_all_characters(), self.cluesolver.get_all_rooms(), self.cluesolver.get_all_weapons(), 5)
        if guess:
            self.cluesolver.make_guess(player, guess)

    def create_player_buttons(self, title, num_items=None):
        # Create a new Toplevel window
        new_window = tk.Toplevel(self)
        new_window.geometry("300x400")
        new_window.title(title)
        players = self.cluesolver.get_players()
        for player in players:
            button = tk.Button(new_window, text=player, command=lambda player=player, new_window=new_window: [self.create_player_menu(f"{player} menu", player, new_window), new_window.destroy()], padx=10, pady=5)
            button.pack(pady=10)

    def change_player_name(self, title, player):
        new_name = simpledialog.askstring(title, f"Type the new player name.", parent=self)
        self.cluesolver.rename_player(player, new_name)
        return None

    def create_player_menu(self, title, player, new_window):
        new_window = tk.Toplevel(self)
        new_window.geometry("300x600")
        new_window.title(title)
        button_change_player_name = tk.Button(new_window, text="Change Name", command=lambda player=player, new_window=new_window: [self.change_player_name_button_click(title, player, new_window), new_window.destroy()], padx=10, pady=10)
        button_change_player_name.pack(pady=10)

        button_saw_item = tk.Button(new_window, text="Player Showed Card", command=lambda player=player, new_window=new_window: [self.showed_item_button_click(player), new_window.destroy()], padx=10, pady=10)
        button_saw_item.pack(pady=10)

        button_heard_guess = tk.Button(new_window, text="Player Guess", command=lambda player=player, new_window=new_window: [self.heard_guess_button_click(player), new_window.destroy()], padx=10, pady=10)
        button_heard_guess.pack(pady=10)

        button_shown_known_cards = tk.Button(new_window, text="Show Players Known Cards", command=lambda player=player, new_window=new_window: [self.print_known_cards_button_click(player), new_window.destroy()], padx=10, pady=10)
        button_shown_known_cards.pack(pady=10)

        button_shown_guesses_ = tk.Button(new_window, text="Show Players Guesses", command=lambda player=player, new_window=new_window: [self.print_player_guesses_button_click(player), new_window.destroy()], padx=10, pady=10)
        button_shown_guesses_.pack(pady=10)

        button_start_cards = tk.Button(new_window, text="Players Start Cards", command=lambda player=player, new_window=new_window: [self.start_cards_button_click(player)], padx=10, pady=10)
        button_start_cards.pack(pady=10)

        button_delete_player = tk.Button(new_window, text="Delete Player", command=lambda player=player, new_window=new_window: [self.delete_player_button_click(player), new_window.destroy()], padx=10, pady=10)
        button_delete_player.pack(pady=10)

        return None

    def change_player_name_button_click(self, title, player, new_window):
        self.change_player_name(title, player)

    def delete_player_button_click(self, player):
        self.cluesolver.delete_player(player)

    def create_item_buttons(self, title, player, items, num_items=None):
        # Create a new Toplevel window
        new_window = tk.Toplevel(self)
        new_window.geometry("300x600")
        new_window.title(title)

        players = self.cluesolver.get_players()
        
        showedPlayer = self.choose_item_for_guess('Choose Player Saw This Card', players)
        
        for item in items:
            button = tk.Button(new_window, text=item, command=lambda player=player, item=item, showedPlayer=showedPlayer, new_window=new_window: [self.saw_player_card(player, item, showedPlayer), new_window.destroy()])
            button.pack(pady=1)

    def delete_start_cards(self, title, player, items, num_items=None):
        # Create a new Toplevel window
        new_window = tk.Toplevel(self)
        new_window.geometry("300x600")
        new_window.title(title)
        
        for item in items:
            button = tk.Button(new_window, text=item, command=lambda player=player, item=item, new_window=new_window: [self.remove_start_cards(player, item), new_window.destroy()])
            button.pack(pady=1)

    def start_cards_button_click(self, player):
        items = self.cluesolver.get_unknown_characters() + self.cluesolver.get_unknown_rooms() + self.cluesolver.get_unknown_weapons()
        self.delete_start_cards('Starting Cards', player, items)

    def saw_player_card(self, player, item, showedPlayer):
        self.cluesolver.saw_card(player, item, showedPlayer)

    def remove_start_cards(self, player, card):
        self.cluesolver.remove_game_start_cards(player, card)

    def print_known_cards_button_click(self, player):
        self.cluesolver.show_player_known_cards(player)

    def print_player_guesses_button_click(self, player):
        self.cluesolver.show_player_guess_list(player)

    def print_ptable_button_click(self):
        self.cluesolver.show_probability_table()


    def choose_item_from_list(self, title, items):
        item = simpledialog.askstring(title, "Choose an item:", initialvalue=items[0], parent=self)
        if item and item in items:
            return item
        return None

    def choose_items_from_list(self, title, chars, rooms, weps, num_items):
        players = self.cluesolver.get_players()
        
        player = self.choose_item_for_guess('Choose Player That Guessed', players)
        character = self.choose_item_for_guess('Choose a Character', chars)
        room = self.choose_item_for_guess('Choose a Room', rooms)
        weapon = self.choose_item_for_guess('Choose a Weapon', weps)
        showedCard = tk.StringVar()
        # Create a new Toplevel window for the boolean value
        new_window = tk.Toplevel(self)
        new_window.geometry("300x600")
        new_window.title("Player Showed a Card")

        def update_and_close(bool):
            showedCard.set(bool)
            new_window.destroy()
        for value in ['true', 'false']:
            button = tk.Button(new_window, text=value, command=lambda value=value: update_and_close(value), padx=10, pady=10)
            button.pack(pady=10)

        # Wait for the user to close the window
        self.wait_window(new_window)
        guess = (character, room, weapon, showedCard.get(), player)
        # Check if the correct number of items were selected
        if len(guess) != num_items:
            return None
        return guess
    
    def choose_item_for_guess(self, title, items):
        selected_item = tk.StringVar()
        new_window = tk.Toplevel(self)
        new_window.geometry("300x600")
        new_window.title(title)

        def update_and_close(item):
            selected_item.set(item)
            new_window.destroy()

        for item in items:
            button = tk.Button(new_window, text=item, command=lambda item=item, items=items: update_and_close(item), padx=10, pady=10)
            button.pack(pady=10)

        self.wait_window(new_window)

        return selected_item.get()

    def get_best_guess_button_click(self):
        self.cluesolver.get_best_guess()

    def clr_console_button_click(self):
        self.cluesolver.clear_console()


def main():
    app = ClueSolverGUI()
    app.mainloop()

if __name__ == "__main__":
    main()