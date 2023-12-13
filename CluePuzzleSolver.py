from itertools import product

class TruthTable:
    def __init__(self, rooms, characters, weapons):
        self.rooms = rooms
        self.characters = characters
        self.weapons = weapons
        self.clue_truth_table = self.generate_truth_table()

    def generate_truth_table(self):
        card_combinations = list(product(self.rooms, self.characters, self.weapons))
        truth_table = [{'Room': combo[0], 'Character': combo[1], 'Weapon': combo[2]} for combo in card_combinations]
        return truth_table

    def remove_row_at_index(self, index):
        if self.clue_truth_table is not None and 0 <= index < len(self.clue_truth_table):
            return self.clue_truth_table.pop(index)

    def __len__(self):
        return len(self.clue_truth_table)

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self.clue_truth_table is not None and self._index < len(self.clue_truth_table):
            result = self.clue_truth_table[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration

class ClueSolver:
    def __init__(self, rooms, characters, weapons):
        self.probability_table = {
            'Room': {},
            'Characters': {},
            'Weapons': {},
        }
        self.truth_table = TruthTable(rooms, characters, weapons)
        self.set_probabilities(rooms, characters, weapons)

    def set_probabilities(self, rooms, characters, weapons):
        for room in rooms:
            self.probability_table['Room'].update({room: 1/9})

        for char in characters:
            self.probability_table['Characters'].update({char: 1/6})

        for wep in weapons:
            self.probability_table['Weapons'].update({wep: 1/6})

    def update_probability_table(self, item):
        TheRoom = self.probability_table["Room"]
        TheChar = self.probability_table["Characters"]
        TheWep = self.probability_table["Weapons"]
        if item in TheRoom:
            prob = TheRoom[item]
            TheRoom.pop(item)
            prob = prob/len(TheRoom)
            for keys in TheRoom:
                TheRoom[keys] += prob
        if item in TheChar:
            prob = TheChar[item]
            TheChar.pop(item)
            prob = prob/len(TheChar)
            for keys in TheChar:
                TheChar[keys] += prob
        if item in TheWep:
            prob = TheWep[item]
            TheWep.pop(item)
            prob = prob/len(TheWep)
            for keys in TheWep:
                TheWep[keys] += prob

    def update_probability_table2(self, room, character, weapon):
        TheRoom = self.probability_table["Room"]
        TheChar = self.probability_table["Characters"]
        TheWep = self.probability_table["Weapons"]
        rProb = self.get_item_prob(room, 1)
        cProb = self.get_item_prob(character, 2)
        wProb = self.get_item_prob(weapon, 3)
        for item in self.probability_table["Room"]:
            if (item == room):
                TheRoom[item] -= rProb
            if (item != room):
                TheRoom[item] += rProb
        for item in self.probability_table["Characters"]:
            if (item == character):
                TheChar[item] -= cProb
            if (item != character):
                TheChar[item] += cProb
        for item in self.probability_table["Weapons"]:
            if (item == weapon):
                TheWep[item] -= wProb
            if (item != weapon):
                TheWep[item] += wProb

    def get_item_prob(self, item, type):
        i = 0
        if (type == 1):
            for row in self.truth_table:
                if (row['Room'] == item):
                    i += 1
            prob = i/len(self.truth_table)
            diff = ((i+1)/len(self.truth_table)) - prob
            return diff

        elif (type == 2):
            for row in self.truth_table:
                if (row['Character'] == item):
                    i += 1
            prob = i/len(self.truth_table)
            diff = ((i+1)/len(self.truth_table)) - prob
            return diff
        else:
            for row in self.truth_table:
                if (row['Weapon'] == item):
                    i += 1
            prob = i/len(self.truth_table)
            diff = ((i+1)/len(self.truth_table)) - prob
            return diff

    def update_truth_table1(self, item):
        indexes_to_remove = []
        i = 0
        for row in self.truth_table:
            if (row['Room'] == item):
                indexes_to_remove.append(i)
            if (row['Character'] == item):
                indexes_to_remove.append(i)
            if (row['Weapon'] == item):
                indexes_to_remove.append(i)
            i += 1
        indexes_to_remove.sort(reverse=True)
        for index in indexes_to_remove:
            self.truth_table.remove_row_at_index(index)

    def update_truth_table2(self, room, character, weapon):
        i = 0
        found = False
        for row in self.truth_table:
            if (row['Room'] == room and row['Character'] == character and row['Weapon'] == weapon):
                found = True
                break
            i += 1
            
        if (found):
            self.truth_table.remove_row_at_index(i)
            self.update_probability_table2(room, character, weapon)
        else:
            print("Did Not Find")
            roomIs = True
            characterIs = True
            weaponIs = True
            if self.probability_table["Room"].get(room) is not None:
                roomIs = False
            if self.probability_table["Characters"].get(character) is not None:
                characterIs = False
            if self.probability_table["Weapons"].get(weapon) is not None:
                weaponIs = False
            if (roomIs and characterIs and weaponIs):
                return
            elif (roomIs and characterIs):
                self.update_probability_table(weapon)
                self.update_truth_table1(weapon)
            elif (roomIs and weaponIs):
                self.update_probability_table(character)
                self.update_truth_table1(character)
            elif (characterIs and weaponIs):
                self.update_probability_table(room)
                self.update_truth_table1(room)
    
    def saw_item(self, item):
        self.update_probability_table(item)
        self.update_truth_table1(item)

    def heard_item(self, room, character, weapon):
        self.update_truth_table2(room, character, weapon)

    def print_probability_tables(self):
        print(self.probability_table['Characters'])
        print()
        print(self.probability_table['Weapons'])
        print()
        print(self.probability_table['Room'])

    def print_truth_table(self):
        for row in self.truth_table:
            print(row)
    

# SawItem("Colonel Mustard")
# SawItem("Revolver")
# SawItem("Kitchen")
# SawItem("Lounge")
# SawItem("Miss Scarlett")
# SawItem("Library")
# print("\nSaw Mustard, Revolver, Kitchen, Lounge, Miss Scarlet, Library\n")
# printTables()

# print("Guessed Study, Green, Candlestick")
# SawItem("Mr. Green")

# print("Player 2 asked player 3 Conservatory, Miss Scarlett, Rope")
# heard_item("Conservatory", "Miss Scarlett", "Rope" )

# SawItem("Mrs. White")
# print("\nGuessed White, Dining room, Pipe\n")
# print("Saw White")
# # printTables()
# # SawItem("Rope")
# # print("\nSaw Rope\n")

# heard_item("Hall", "Miss Scarlett", "Wrench")
# print("\heard Hall, Scarlett, wrench\n")
# printTables()

# print("\n Guessed Study, Peacock, Wrench")
# SawItem("Study")

# # printTables()

# heard_item("Billiard Room" , "Colonel Mustard", "Revolver")
# print("Player 2 guessed Biliard Room, Colonel Mustard, Revolver and P3 showed a card.")

# heard_item("Dining Room" , "Colonel Mustard", "Revolver")
# print("Player 3 guessed Dining Room, Colonel Mustard, Revolver and P2 showed a card.")

# # printTables()


# print("I asked Player 3  Peachock dagger, in the ball room. and saw Daggar")
# SawItem("Dagger")

# # printTables()

# heard_item("Lounge", "Mrs. Peacock", "Revolver")
# print("I heard Player 3 ask Lounge, Peacock, Revolver and saw player 2 show a card.")

# # printTables()

# print("I asked player 2 Plum in the lounge with the candle stick I saw candle stick")
# SawItem("Candlestick")
# # printTables()

# print("I asked player 3 Conservatory, Plum, Pipe and he showed me conservatory.")
# SawItem("Conservatory")
# printTables()

# print('Player 3 asked Player 2 Ballroom, Miss Scarlet, Dagger Player 2 showed a card.')
# heard_item('Ballroom', "Miss Scarlett", 'Dagger')
# printTables()

# print('I asked player 3 Pipe Scarlett Lounge')
# heard_item('Lounge', "Miss Scarlett", 'Lead Pipe')
# printTables()
