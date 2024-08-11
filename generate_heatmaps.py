import pandas as pd
import string
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(file_path):
    return pd.read_csv(file_path)

def create_boolean_matrix(station_names):
    boolean_matrix = pd.DataFrame(index=station_names, columns=list(string.ascii_uppercase))
    for name in station_names:
        for letter in string.ascii_uppercase:
            boolean_matrix.at[name, letter] = letter in name.upper()
    return boolean_matrix

def generate_heatmap(matrix, title, output_path):
    plt.figure(figsize=(20, 50))
    sns.heatmap(matrix.astype(int), cbar=False, cmap="coolwarm", linewidths=.5)  # Updated cmap for LDN UDG theme
    plt.title(title)
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()

def main():
    file_path = 'LND_UG.csv'
    stations_df = load_data(file_path)
    station_names = stations_df['Station']

    boolean_matrix = create_boolean_matrix(station_names)

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

if __name__ == '__main__':
    main()