

class Player:
    def __init__(self, name):
        self.name = name
        self.has_cards = {
            'Room': {},
            'Characters': {},
            'Weapons': {},}
        self.guesses = [] 
    
    def make_guess(self, guess):
        # Record the player's guess
        self.guesses.append(guess)

    def show_has_cards(self):
        # Print the known cards for the player
        print(f"{self.name}'s Has Cards: {self.has_cards}")

    def update_has_cards(self, card, group):
        self.has_cards[card] = True

    def show_guesses(self):
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

    def guess_update(self, guess):

        c = guess[0]
        r = guess[1]
        w = guess[2]
        showed_card = True

        c_value = self.probability_table.get('Characters', {}).get(c, 0)
        r_value = self.probability_table.get('Rooms', {}).get(r, 0)
        w_value = self.probability_table.get('Weapons', {}).get(w, 0)
        sum_values = c_value + r_value + w_value

        if (not showed_card):
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




    def update_probability_table(self, group, probability):
        # Update the probability table
        self.probability_table[group] = probability

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