# Given equal prior probability for each item within a group
P_Item_in_Group = 1 / 2  # Assuming two items in each group

# Prior probability for each group in the guess
P_Group1_in_Guess = 1 / 3
P_Group2_in_Guess = 1 / 3
P_Group3_in_Guess = 1 / 3

# Calculate the prior probability of the guess
P_Guess = P_Group1_in_Guess * P_Group2_in_Guess * P_Group3_in_Guess

# Calculate the likelihood of the player confirming having one of the guessed items
P_Confirmation_given_Item = 1  # Assuming the player always confirms if they have one of the guessed items

# Update probabilities for each group
P_Group1_given_Guess_and_Confirmation = (P_Confirmation_given_Item * P_Group1_in_Guess) / P_Guess
P_Group2_given_Guess_and_Confirmation = (P_Confirmation_given_Item * P_Group2_in_Guess) / P_Guess
P_Group3_given_Guess_and_Confirmation = (P_Confirmation_given_Item * P_Group3_in_Guess) / P_Guess

# Update probabilities for each item within Group 1
P_Item1_in_Group1_given_Guess_and_Confirmation = (P_Item_in_Group * P_Group1_in_Guess) / P_Guess
P_Item2_in_Group1_given_Guess_and_Confirmation = (P_Item_in_Group * P_Group1_in_Guess) / P_Guess

# Update probabilities for each item within Group 2
P_Item1_in_Group2_given_Guess_and_Confirmation = (1/3 * P_Group2_in_Guess) / P_Guess
P_Item2_in_Group2_given_Guess_and_Confirmation = (1/3 * P_Group2_in_Guess) / P_Guess

# Update probabilities for each item within Group 3
P_Item1_in_Group3_given_Guess_and_Confirmation = (1/3 * P_Group3_in_Guess) / P_Guess
P_Item2_in_Group3_given_Guess_and_Confirmation = (1/3 * P_Group3_in_Guess) / P_Guess

# Sum the probabilities over all groups for each item
P_Item1 = P_Item1_in_Group1_given_Guess_and_Confirmation + P_Item1_in_Group2_given_Guess_and_Confirmation + P_Item1_in_Group3_given_Guess_and_Confirmation
P_Item2 = P_Item2_in_Group1_given_Guess_and_Confirmation + P_Item2_in_Group2_given_Guess_and_Confirmation + P_Item2_in_Group3_given_Guess_and_Confirmation

# Display the updated probabilities
print(f"Updated Probability of Item 1: {P_Item1}")
print(f"Updated Probability of Item 2: {P_Item2}")
