from tkinter import filedialog as fd
import math


def linear_congruential_method(x0, a, c, m, iterations):
    generated_numbers = []
    while iterations != 0:
        x = (a * x0 + c) % m
        r = x / m
        x0 = x
        iterations -= 1
        generated_numbers.append(r)
    print("The numbers are:" + str(generated_numbers))
    return generated_numbers


def chi_squared(file_address):
    data = open(file_address, "r")
    converted_data = []
    for line in data:
        converted_data.append(float(line))
    intervals = 10
    frequencies_intervals = {}
    interval_start = 0.0
    interval_end = 0.1
    interval_growth_factor = interval_end
    for iteration in range(intervals):
        counter = 0
        for number in converted_data:
            if interval_start <= number < interval_end:
                counter += 1
        frequencies_intervals[str(round(interval_start, 4)) + "-" + str(round(interval_end, 4))] = counter
        interval_start += interval_growth_factor
        interval_end += interval_growth_factor
    frequency_table_values = list(frequencies_intervals.values())
    frequency_tables_intervals = list(frequencies_intervals)
    expected_value = len(converted_data) / len(frequency_tables_intervals)
    x = []
    total = 0
    print("Intervals : Observed : Expected : (O-E)^2/E")
    for iteration in range(len(frequency_table_values)):
        x.append(round((frequency_table_values[iteration] - expected_value) ** 2 / expected_value, 4))
        total += x[iteration]
        print(
            "[" + frequency_tables_intervals[iteration] + ") : " + str(frequency_table_values[iteration]) + " : " + str(
                expected_value) + " : " + str(x[iteration]))
    total = round(total, 4)
    print("x^2 = " + str(total))
    if total > 16.91:
        print("Since " + str(total) + " > 16.91, HO is rejected")
    else:
        print("Since " + str(total) + " < 16.91, HO is not rejected")
    return


def runs(file_address):
    data = open(file_address, "r")
    sign_string = ""
    last_number = float
    counter = 0
    for line in data:
        if counter != 0:
            if last_number > float(line):
                sign_string += "-"
            elif last_number < float(line):
                sign_string += "+"
        last_number = float(line)
        counter += 1
    print("Generated signs:")
    print(sign_string)
    total_signs = len(sign_string)
    print("Total signs: " + str(total_signs))
    runs = 1
    counter = 0
    last_char = ""
    for char in sign_string:
        if counter != 0:
            if last_char != char:
                runs += 1
        last_char = char
        counter += 1
    print("Total runs: " + str(runs))
    print("Statistics")
    miu = round((2 * total_signs - 1) / 3, 4)
    sigma = round(math.sqrt((16 * total_signs - 29) / 90), 4)
    zscore = round((runs - miu) / sigma, 4)
    print("Miu: " + str(miu))
    print("Sigma: " + str(sigma))
    print("Zscore: " + str(zscore))
    if zscore < 1.96:
        print("Since |" + str(zscore) + "| < |1.96|, H0 is not rejected")
    else:
        print(print("Since |" + str(zscore) + "| > |1.96|, H0 is rejected"))

    return


def main():
    # linear_congruential_method(6, 32, 3, 80, 10)
    # chi_squared_address = fd.askopenfilename()
    # chi_squared(chi_squared_address)
    runs_address = fd.askopenfilename()
    runs(runs_address)


main()
