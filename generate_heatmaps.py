import pandas as pd
import string
import matplotlib.pyplot as plt
import seaborn as sns
import json
import itertools
from concurrent.futures import ThreadPoolExecutor, as_completed

def load_data(file_path):
    return pd.read_csv(file_path)

def station_name_to_binary(station_name):
    binary_representation = 0
    for letter in station_name.upper():
        if letter in string.ascii_uppercase:
            binary_representation |= 1 << (ord(letter) - ord('A'))
    return binary_representation

def create_boolean_matrix_from_binary(station_binaries, station_names):
    boolean_matrix = pd.DataFrame(index=station_names, columns=list(string.ascii_uppercase))
    for name, binary in zip(station_names, station_binaries):
        for i, letter in enumerate(string.ascii_uppercase):
            boolean_matrix.at[name, letter] = (binary >> i) & 1
    return boolean_matrix

def generate_heatmap(matrix, title, output_path):
    plt.figure(figsize=(20, 50))
    sns.heatmap(matrix.astype(int), cbar=False, cmap="coolwarm", linewidths=.5)
    plt.title(title)
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()

def find_unique_filter_for_station(args):
    idx, name, binary, station_binaries, sorted_letters = args
    letter_set = set(string.ascii_uppercase)
    
    all_other_binaries = station_binaries[:idx] + station_binaries[idx + 1:]
    required_letters = letter_set - set(name.upper())
    
    # List to store all filters
    filters = []

    # Try to find the shortest filter
    for length in range(1, len(required_letters) + 1):
        for combination in itertools.combinations(sorted_letters, length):
            if set(combination).issubset(required_letters):
                if all(any(other & (1 << (ord(letter) - ord('A'))) for letter in combination) for other in all_other_binaries):
                    filters.append(''.join(sorted(combination)))
        
        if filters:
            break

    return (name, filters)

def find_unique_filters(station_names, station_binaries, save_interval=10):
    letter_set = set(string.ascii_uppercase)
    
    # Count the frequency of each letter
    letter_frequency = {letter: 0 for letter in string.ascii_uppercase}
    for binary in station_binaries:
        for letter in string.ascii_uppercase:
            if binary & (1 << (ord(letter) - ord('A'))):
                letter_frequency[letter] += 1

    # Sort letters by frequency from most to least frequent
    sorted_letters = sorted(letter_frequency, key=letter_frequency.get, reverse=True)

    station_filters = {}
    intermediate_save_count = 0  # Counter to track when to save incrementally

    # Create argument list for parallel processing
    args_list = [(idx, name, binary, station_binaries, sorted_letters) for idx, (name, binary) in enumerate(zip(station_names, station_binaries))]

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor() as executor:
        future_to_station = {executor.submit(find_unique_filter_for_station, args): args for args in args_list}

        for future in as_completed(future_to_station):
            name, filters = future.result()
            station_filters[name] = filters
            intermediate_save_count += 1

            # Incremental saving
            if intermediate_save_count % save_interval == 0:
                with open('unique_filters_intermediate.json', 'w') as json_file:
                    json.dump(station_filters, json_file, indent=4)

    # Final save
    with open('unique_filters.json', 'w') as json_file:
        json.dump(station_filters, json_file, indent=4)

    return station_filters

def query_station_names(letter_combination, station_names):
    letter_set = set(letter_combination.upper())
    matched_stations = [name for name in station_names if letter_set.issubset(set(name.upper()))]

    return matched_stations

def main():
    file_path = 'LND_UG.csv'
    stations_df = load_data(file_path)
    station_names = stations_df['Station']

    # Convert station names to binary representations
    station_binaries = [station_name_to_binary(name) for name in station_names]
    
    # Create the boolean matrix from binary representations
    boolean_matrix = create_boolean_matrix_from_binary(station_binaries, station_names)

    # Alphabetically sorted heatmap
    alphabetically_sorted_matrix = boolean_matrix.sort_index()
    generate_heatmap(alphabetically_sorted_matrix, 'Alphabetically Sorted Station Names', 
                     'london_underground_station_heatmap_alphabetical.png')

    # Frequency sorted heatmap
    letter_frequency = {letter: sum(boolean_matrix[letter]) for letter in string.ascii_uppercase}
    sorted_letters = sorted(letter_frequency, key=letter_frequency.get, reverse=True)
    sorted_boolean_matrix = boolean_matrix[sorted_letters].sort_values(by=sorted_letters, ascending=False)
    generate_heatmap(sorted_boolean_matrix, 'Frequency Sorted Station Names', 
                     'london_underground_station_heatmap_frequency.png')

    # Reverse frequency sorted heatmap (rarest letters at the top)
    reverse_sorted_letters = sorted(letter_frequency, key=letter_frequency.get)
    reverse_sorted_boolean_matrix = boolean_matrix[reverse_sorted_letters].sort_values(by=reverse_sorted_letters, ascending=True)
    generate_heatmap(reverse_sorted_boolean_matrix, 'Reverse Frequency Sorted Station Names', 
                     'london_underground_station_heatmap_reverse_frequency.png')

    # Find unique filters for each station and save them in an array to a JSON file
    unique_filters = find_unique_filters(station_names, station_binaries)

    with open('unique_filters.json', 'w') as json_file:
        json.dump(unique_filters, json_file, indent=4)

    # Example query station names based on letter combination
    queried_stations = query_station_names('AEIOU', station_names)
    print("Stations containing 'AEIOU':", queried_stations)

if __name__ == '__main__':
    main()