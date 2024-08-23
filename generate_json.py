import os
import json
import base64
import string
import pandas as pd
from pathlib import Path
import combined_filter_finder

def convert_to_binary_mask(word):
    binary_mask = 0
    for char in word.upper():
        if 'A' <= char <= 'Z':
            binary_mask |= 1 << (ord(char) - ord('A'))
    return binary_mask

def sanitize_station_name(station_name):
    sanitized = ''.join(sorted(set(char for char in station_name.upper() if char in string.ascii_uppercase)))
    return sanitized

def load_base64_file(file_path='base64.txt'):
    if not Path(file_path).exists():
        print(f"Error: {file_path} not found. Please run txt_to_binary.py first.")
        exit(1)
    
    binary_rep_list = bytearray(base64.b64decode(Path(file_path).read_text(encoding='utf-8').strip()))
    
    word_list = []
    binary_word_map = {}
    with open('130k.txt', 'r', encoding='utf-8') as f:
        for word, bytes_chunk in zip(f, [binary_rep_list[i:i+4] for i in range(0, len(binary_rep_list), 4)]):
            word = word.strip()
            binary_rep = int.from_bytes(bytes_chunk, 'big')
            word_list.append(word)
            binary_word_map[word] = binary_rep
            
    return word_list, binary_word_map

def find_top_words_for_filters(word_list, binary_word_map, filters, target_stations, top_n=2):
    results = {}

    target_bits = [convert_to_binary_mask(sanitize_station_name(station)) for station in target_stations]

    for filter_entry in filters:
        filter_name = filter_entry['filter'] if isinstance(filter_entry, dict) else filter_entry
        print(f"Processing filter: {filter_name}")  # Debug statement
        filter_bits = convert_to_binary_mask(filter_name)

        top_words = []
        print(f"Finding top words for filter: {filter_name}")
        for word, binary_mask in binary_word_map.items():
            if (binary_mask & filter_bits == filter_bits and 
                all(binary_mask & tb == 0 for tb in target_bits)):
                top_words.append(word)
                if len(top_words) == top_n:
                    break

        results[filter_name] = top_words

    return results

def read_and_merge_csv(file_paths):
    all_stations_set = set()
    for file_path in file_paths:
        df = pd.read_csv(file_path)
        stations = df['Station'].tolist()
        all_stations_set.update(stations)
    return list(all_stations_set)

def main():
    word_list, binary_word_map = load_base64_file()

    file_paths = ["LND_UG.csv"]  # Include any additional CSV files if available
    all_stations = read_and_merge_csv(file_paths)

    result_data = []

    for target_station in all_stations:
        print(f"Processing station: {target_station}")
        
        combined_result = combined_filter_finder.combined_filter_finder(file_paths=file_paths, target_stations=[target_station])
        station_results = json.loads(combined_result)[0]

        station_data = {
            "target_station": target_station,
            "unique_filters": [],
            "narrowed_down_filters": []
        }
        
        # Process unique filters
        unique_filters = station_results['unique_filters']
        print(f"Processing unique filters for station: {target_station}")
        unique_top_words = find_top_words_for_filters(word_list, binary_word_map, unique_filters, [target_station])
        
        for f in unique_filters:
            f['top_words'] = unique_top_words[f['filter']]
        
        station_data['unique_filters'] = unique_filters

        # Process narrowed down filters
        narrowed_down_filters = station_results['narrowed_down_filters']
        print(f"Processing narrowed down filters for station: {target_station}")
        narrowed_top_words = find_top_words_for_filters(word_list, binary_word_map, narrowed_down_filters, [target_station])
        
        for entry in narrowed_down_filters:
            entry['top_words'] = narrowed_top_words[entry['filter']]
        
        station_data['narrowed_down_filters'] = narrowed_down_filters

        result_data.append(station_data)
    
    # Save the result data into unique_filters.json
    output_file = 'unique_filters.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, indent=4)

    print(json.dumps(result_data, indent=4))

if __name__ == "__main__":
    main()