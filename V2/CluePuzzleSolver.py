import os

class Player:
    def __init__(self, name):
        self.name = name
        self.known_cards = {
            'Rooms': {},
            'Characters': {},
            'Weapons': {},}
        self.guesses = [] 

    def get_name(self):
        return self.name
    
    def get_number_of_guesses(self):
        return len(self.guesses)
    
    def get_guess_list(self):
        return self.guesses
    
    def get_number_of_known_cards(self):
        c = len(self.known_cards["Characters"])
        r = len(self.known_cards["Rooms"])
        w = len(self.known_cards["Weapons"])
        return c + r + w
    
    def change_player_name(self, new_name):
        self.name = new_name
    
    def make_guess(self, guess):
        # Record the player's guess
        self.guesses.append(guess)

    def show_known_cards(self):
        # Print the known cards for the player
        print(f"{self.name}'s known cards: {self.known_cards}")

    def update_known_cards(self, card, group):
        # Updates the known cards for this player
        self.known_cards[group][card] = True

    def show_guesses(self):
        # Shows what guesses have been guessed on this player
        print(f"{self.name} has these guesses:\n")
        for guess in self.guesses:
            print(guess)
            

class ProbabilityTable:
    def __init__(self, chars, rooms, weps):
        self.probability_table = {
            'Characters': {},
            'Rooms': {},
            'Weapons': {},
        }
        self.initialize_probability_table(chars, rooms, weps)

    def __getitem__(self, key):
        # Implement the __getitem__ method to allow subscripting
        return self.probability_table[key]

    def initialize_probability_table(self, characters, rooms, weapons):
        for char in characters:
            self.probability_table['Characters'].update({char: 1/6})
        for room in rooms:
            self.probability_table['Rooms'].update({room: 1/9})

        for wep in weapons:
            self.probability_table['Weapons'].update({wep: 1/6})

    def show_probability_table(self):
        # Print the probability table for the player
        print(f"Characters: {self.probability_table['Characters']}\n")
        print(f"Rooms: {self.probability_table['Rooms']}\n")
        print(f"Weapons: {self.probability_table['Weapons']}\n")

    def remove_item_from_table(self, group, item):
        self.probability_table.get(group, {}).pop(item)
        self.normalize_table(group)

    def guess_update(self, guess):

        c = guess[0]
        r = guess[1]
        w = guess[2]
        showed_card = guess[3].lower()

        c_value = self.probability_table.get('Characters', {}).get(c, 0)
        r_value = self.probability_table.get('Rooms', {}).get(r, 0)
        w_value = self.probability_table.get('Weapons', {}).get(w, 0)
        sum_values = c_value + r_value + w_value

        if (showed_card == "false"):
            if (c_value != 0):
                c_value /= sum_values
                self.probability_table['Characters'][c] = c_value
                self.normalize_table('Characters')
            if (r_value != 0):
                r_value /= sum_values
                self.probability_table['Rooms'][r] = r_value
                self.normalize_table('Rooms')
            if (w_value != 0):
                w_value /= sum_values
                self.probability_table['Weapons'][w] = w_value
                self.normalize_table('Weapons')
        else:
            if (c_value != 0):
                c_value *= sum_values
                self.probability_table['Characters'][c] = c_value
                self.normalize_table('Characters')
            if (r_value != 0):    
                r_value *= sum_values
                self.probability_table['Rooms'][r] = r_value
                self.normalize_table('Rooms')
            if (w_value != 0):
                w_value *= sum_values
                self.probability_table['Weapons'][w] = w_value
                self.normalize_table('Weapons')

    def normalize_table(self, group):
        total_sum = sum(self.probability_table[group].values())
        for key in self.probability_table[group]:
                self.probability_table[group][key] /= total_sum

                #The Formula for bayes
        #for each guess I will take all the items in the guess
        #I will then add there three probabilities off the table.
        # for each node or item class 
        #I will then divide the original % for each item on the table 
        # by the combined amount of the 3 guesses table probabilities.

        #Then I will normilize the table for each value
        # formula table value = old value / old values added.
        # I will probably have to create a copy dictionary or list to do this and then update the table 


class ClueSolver:
    def __init__(self):
        self.characters = ["mustard", "scarlett", "plum", "peacock", "green","orchid"]
        self.weapons = ["candlestick", "dagger", "pipe", "revolver", "rope", "wrench"]
        self.rooms = ["kitchen", "ballroom", "conservatory", "dining", "billiard", "library", "lounge", "hall", "study"]
        self.unknown_characters = ["mustard", "scarlett", "plum", "peacock", "green","orchid"]
        self.unknown_weapons = ["candlestick", "dagger", "pipe", "revolver", "rope", "wrench"]
        self.unknown_rooms = ["kitchen", "ballroom", "conservatory", "dining", "billiard", "library", "lounge", "hall", "study"]
        self.p_table = ProbabilityTable(self.characters, self.rooms, self.weapons)
        player1 = Player('player1')
        player2 = Player('player2')
        player3 = Player('player3')
        player4 = Player('player4')
        player5 = Player('player5')
        self.players = {'player1': player1, 'player2': player2,'player3': player3, 'player4': player4, 'player5': player5}

    def get_all_characters(self):
        return self.characters
    
    def get_all_rooms(self):
        return self.rooms
    
    def get_all_weapons(self):
        return self.weapons
    
    def get_unknown_characters(self):
        return self.unknown_characters
    
    def get_unknown_rooms(self):
        return self.unknown_rooms
    
    def get_unknown_weapons(self):
        return self.unknown_weapons
    
    def get_players(self):
        list_of_players = []
        for player in self.players:
            list_of_players.append(player)
        return list_of_players

    def get_player(self, player):
        for p in self.players:
            if (player == p):
                return p
            else:
                return -1
            
    def get_all_known_cards(self):        
        for player in self.players:
            self.players[player].show_known_cards()

    
    def show_player_guess_list(self, player):
        self.players[player].show_guesses()

    def show_player_known_cards(self, player):
        self.players[player].show_known_cards()
        
    def make_guess(self, player, guess):
        self.players[player].make_guess(guess)
        self.p_table.guess_update(guess)

    def saw_card(self, player, card):
        group = "Rooms"
        if card in self.p_table["Characters"]:
            group = "Characters"
        elif card in self.p_table["Weapons"]:
            group = "Weapons"

        self.players[player].update_known_cards(card, group)
        self.p_table.remove_item_from_table(group, card)
        if card in self.unknown_characters:
            self.unknown_characters.remove(card)
        elif card in self.unknown_rooms:
            self.unknown_rooms.remove(card)
        elif card in self.unknown_weapons:
            self.unknown_weapons.remove(card)

    def unsee_card(self, card, group):
        print("out of luck right now feature to come.")

    def rename_player(self, player, new_name):
        self.players[new_name] = self.players.pop(player)
        self.players[new_name].name = new_name

    def delete_player(self, player):
        self.players.pop(player)
    
    def show_probability_table(self):
        return self.p_table.show_probability_table()
    
    def get_best_guess(self):
        max_char = max(self.p_table["Characters"].values(), self.p_table["Characters"].get)
        max_char_value = max(self.p_table["Characters"].values())
        max_room = max(self.p_table["Rooms"].values(), self.p_table["Rooms"].get)
        max_room_value = max(self.p_table["Rooms"].values())
        max_wep = max(self.p_table["Weapons"].values(), self.p_table["Weapons"].get)
        max_wep_value = max(self.p_table["Weapons"].values())

        print(f'The highest probablity guess is {max_char} in the {max_room} with the {max_wep}\n')
        print(f'{max_char} - {max_char_value:.0%} {max_room} - {max_room_value:.0%} {max_wep} - {max_wep_value:.0%}')
        player_with_least_known_cards = ""
        min_shown_cards = 100

        for player in self.players:
            guess_list = player.get_guess_list()
            if (player.get_number_of_known_cards < min_shown_cards):
                min_shown_cards = player.get_number_of_known_cards
                player_with_least_known_cards = player.get_name
            for guess in guess_list:
                if (guess[0] == max_char and guess[1] == max_room and guess[2] == max_wep and guess[3] == True):
                    print(f"Player: {player.get_name()} has been asked this and show a card.\n")
        
        print(f"{player_with_least_known_cards} has the least amount of known cards.\n")
        print("Hope this helps.")

    def clear_console(self):
        os.system('cls')
                