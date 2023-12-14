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
        print(f"Removed item: {item}")

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
                print(f"Deleted weapon: {weapon}")
                self.update_probability_table(weapon)
                self.update_truth_table1(weapon)
            elif (roomIs and weaponIs):
                print(f"Deleted character: {character}")
                self.update_probability_table(character)
                self.update_truth_table1(character)
            elif (characterIs and weaponIs):
                print(f"Deleted room: {room}")
                self.update_probability_table(room)
                self.update_truth_table1(room)
            elif (roomIs and not characterIs and not weaponIs):
                self.update_truth_table3(1, character, weapon)
            elif (not roomIs and characterIs and not weaponIs):
                self.update_truth_table3(2, room, weapon)
            elif(not roomIs and not characterIs and weaponIs):
                self.update_truth_table3(3, room, character)

    def update_truth_table3(self, type, unknown1, unknown2):
        indexes_to_remove = []
        i = 0
        for row in self.truth_table:
            if (type == 1):
                if (row['Character'] == unknown1 and row['Weapon'] == unknown2):
                    indexes_to_remove.append(i)
            if (type == 2):
                if (row['Room'] == unknown1 and row['Weapon'] == unknown2):
                    indexes_to_remove.append(i)
            if (type == 3):
                if (row['Room'] == unknown1 and row['Character'] == unknown2):
                    indexes_to_remove.append(i)
            i += 1
        indexes_to_remove.sort(reverse=True)
        for index in indexes_to_remove:
            self.truth_table.remove_row_at_index(index)
        if (type == 1):
            cdiff = self.get_item_prob(unknown1, type)
            wdiff = self.get_item_prob(unknown2, type)
            self.update_probability_table3(unknown1, type, cdiff)
            self.update_probability_table3(unknown2, type, wdiff)
        elif (type == 2):
            rdiff = self.get_item_prob(unknown1, type)
            wdiff = self.get_item_prob(unknown2, type)
            self.update_probability_table3(unknown1, type, rdiff)
            self.update_probability_table3(unknown2, type, wdiff)
        elif (type == 3):
            rdiff = self.get_item_prob(unknown1, type)
            cdiff = self.get_item_prob(unknown2, type)
            self.update_probability_table3(unknown1, type, rdiff)
            self.update_probability_table3(unknown2, type, cdiff)
        
        print(f"Removed {len(indexes_to_remove)} total items with {unknown1} and {unknown2}")
    
    def update_probability_table3(self, item, type, rdiff=0, cdiff=0, wdiff=0):
        TheRoom = self.probability_table["Room"]
        TheChar = self.probability_table["Characters"]
        TheWep = self.probability_table["Weapons"]
        if (type != 1):
            for table_item in self.probability_table["Room"]:
                if (item == table_item):
                    TheRoom[table_item] -= rdiff
                if (item != item):
                    TheRoom[table_item] += rdiff
        if (type != 2):
            for table_item in self.probability_table["Characters"]:
                if (item == table_item):
                    TheChar[table_item] -= cdiff
                if (item != item):
                    TheChar[table_item] += cdiff
        if (type != 3):
            for table_item in self.probability_table["Weapons"]:
                if (item == table_item):
                    TheWep[table_item] -= wdiff
                if (item != item):
                    TheWep[table_item] += wdiff


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