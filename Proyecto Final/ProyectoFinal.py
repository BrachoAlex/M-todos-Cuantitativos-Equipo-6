import random
import pandas as pd
from contextlib import redirect_stdout


def generate_matrix(n, warrior_group_list):
    matrix = {}
    for i in range(n):
        data = []
        probability = 1
        for a in range(n):
            # Same group
            if a == i:
                number = 0
            else:
                if a == n - 1 or (a == i - 1 and a == n - 2):
                    last = 0
                    for entry in data:
                        last += entry
                    number = abs(round(1 - last, 2))
                else:
                    if len(data) == 0:
                        number = abs(round(random.uniform(0, 1), 2))
                    else:
                        number = abs(round(random.uniform(0, probability), 2))
            probability -= number
            data.append(number)
        matrix[warrior_group_list[i]] = data
    return matrix


def mortal_battle_markov_chains(matrix, warriors_number_detail_per_group, warrior_group_list):
    # 0 value means a group is annihilated.
    while 0 not in warriors_number_detail_per_group.values():
        attacking_group = random.choice(warrior_group_list)
        chances_converted = []
        repetition_list = []
        # This loop "converts" decimal numbers to int nums, useful for filling a list and then random choice that list.
        for chance in matrix[attacking_group]:
            # chance is decimal.
            chances_converted.append(int(chance * 100))
        index = 0
        # Fills repetition list with index * n number of times, n = 1%. List length is 100, 100%
        for number in chances_converted:
            c = 1
            while c <= number:
                repetition_list.append(warrior_group_list[index])
                c += 1
            index += 1
        attacked_group = random.choice(repetition_list)
        print("")
        print("Group " + str(attacking_group) + " attacked Group " + str(attacked_group) + "!")
        warriors_number_detail_per_group[attacked_group] -= 1
        print("Number of warriors for each group:")
        for key in warrior_group_list:
            print("Group " + str(key) + ": " + str(warriors_number_detail_per_group[key]))
    beaten_group = -1
    for i in warriors_number_detail_per_group:
        if warriors_number_detail_per_group[i] == 0:
            beaten_group = i
    return beaten_group


def main():
    # Program works with n size matrix.
    matrix_size = int(input("Enter the desired matrix size: "))
    army_size_max = int(input("Enter the maximum number of warriors per group: "))
    # Output is redirected to file.
    with open('out.txt', 'w') as f:
        with redirect_stdout(f):
            # ID of each group. Edited later when a group loses.
            warrior_group_list = [*range(1, matrix_size + 1)]
            # Dictionary containing warrior number for each group.
            warriors_number_detail_per_group = {}
            # Random warrior generator per group.
            for i in range(len(warrior_group_list)):
                warriors = random.randint(1, army_size_max)
                warriors_number_detail_per_group[warrior_group_list[i]] = warriors
            # Main loop limited by matrix size. Matrix size 1 means a winner is determined.
            while matrix_size > 1:
                matrix = generate_matrix(matrix_size, warrior_group_list)
                table = pd.DataFrame.from_dict(matrix, orient='index', columns=matrix.keys())
                print(table)
                print("Number of warriors for each group:")
                # Printing number of warriors per group.
                for group in warrior_group_list:
                    print("Group " + str(group) + ": " + str(warriors_number_detail_per_group[group]))
                print("=================================")
                beaten_group = mortal_battle_markov_chains(matrix, warriors_number_detail_per_group, warrior_group_list)
                print("Group " + str(beaten_group) + " is annihilated!")
                print("*********************************")
                # Delete group for id list and army number info.
                del warriors_number_detail_per_group[beaten_group]
                warrior_group_list.remove(beaten_group)
                # Check matrix size to determine next step.
                if len(warrior_group_list) == 1:
                    print("Group " + str(warrior_group_list[0]) + " is the winner!")
                    break
                else:
                    print("Reconfiguring stochastic matrix:")
                # A group is beaten, so matrix size shrinks.
                matrix_size -= 1
    print("Operation completed, please check out.txt")


main()
