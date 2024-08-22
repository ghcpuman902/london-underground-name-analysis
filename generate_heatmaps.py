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
    ax = sns.heatmap(matrix.astype(int), cbar=False, cmap="coolwarm", linewidths=.5)
    plt.title(title, fontsize=16, pad=20)
    
    # Add letter labels at the top
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    plt.xticks(fontsize=8, rotation=0)
    
    # Add letter labels at the bottom
    ax2 = ax.twiny()
    ax2.set_xlim(ax.get_xlim())
    ax2.set_xticks(ax.get_xticks())
    ax2.set_xticklabels(ax.get_xticklabels())
    plt.xticks(fontsize=8, rotation=0)
    
    # Adjust layout to prevent cutting off labels
    plt.tight_layout()
    
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()

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
    reverse_sorted_boolean_matrix = boolean_matrix[reverse_sorted_letters].sort_values(by=reverse_sorted_letters, ascending=True).iloc[::-1]
    generate_heatmap(reverse_sorted_boolean_matrix, 'Reverse Frequency Sorted Station Names', 
                     'london_underground_station_heatmap_reverse_frequency.png')


if __name__ == '__main__':
    main()