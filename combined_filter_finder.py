# combined_filter_finder.py

import json
import os
import pandas as pd
import string
import time
from collections import Counter
from itertools import combinations

def sanitize_station_name(station_name):
    sanitized = ''.join([char for char in station_name.upper() if char in string.ascii_uppercase])
    return sanitized

def convert_to_binary_mask(station_name):
    binary_mask = 0
    for char in station_name:
        binary_mask |= 1 << (ord(char) - ord('A'))
    return binary_mask

def shares_letter_with_all(filter_mask, station_masks, station_mask_to_remove):
    station_masks = [mask for mask in station_masks if mask != station_mask_to_remove]
    for mask in station_masks:
        if filter_mask & mask == 0:
            return False
    return True

def preprocess_station_names(station_names):
    sanitized_names = []
    binary_masks = []
    letter_frequencies = Counter()
    sanitized_to_original = {}

    for station_name in station_names:
        sanitized_name = sanitize_station_name(station_name)
        sanitized_names.append(sanitized_name)
        mask = convert_to_binary_mask(sanitized_name)
        binary_masks.append(mask)
        letter_frequencies.update(sanitized_name)
        sanitized_to_original[sanitized_name] = station_name

    return sanitized_names, binary_masks, letter_frequencies, sanitized_to_original

def find_best_filters_optimized(sanitized_names, binary_masks, letter_frequencies, target_station_name):
    start_time = time.time()

    sanitized_target = sanitize_station_name(target_station_name)
    target_index = sanitized_names.index(sanitized_target)
    target_mask = convert_to_binary_mask(sanitized_target)
    target_letters = set(sanitized_target)

    all_other_letters = set(letter_frequencies.keys()) - target_letters
    possible_filters = [letter for letter, _ in letter_frequencies.most_common() if letter in all_other_letters]

    best_length = None
    best_filters = []

    for i in range(1, len(possible_filters) + 1):
        for combination in combinations(possible_filters, i):
            filter_mask = convert_to_binary_mask(''.join(combination))

            if shares_letter_with_all(filter_mask, binary_masks, target_mask):
                if best_length is None:
                    best_length = i
                if i == best_length:
                    best_filters.append(''.join(combination))
                elif i > best_length:
                    elapsed_time = time.time() - start_time
                    return best_filters, elapsed_time

    elapsed_time = time.time() - start_time
    return best_filters, elapsed_time

def find_narrowed_down_filters(sanitized_names, binary_masks, target_station_name, sanitized_to_original):
    start_time = time.time()
    sanitized_target = sanitize_station_name(target_station_name)
    target_index = sanitized_names.index(sanitized_target)
    target_mask = convert_to_binary_mask(sanitized_target)

    all_letters = set(string.ascii_uppercase)
    
    narrowed_down_filters = []

    for i in range(1, 5):
        for combination in combinations(all_letters, i):
            filter_mask = convert_to_binary_mask(''.join(combination))
            non_matching_indices = [index for index, mask in enumerate(binary_masks) if filter_mask & mask == 0]

            if target_index in non_matching_indices and len(non_matching_indices) <= 5:
                matching_stations = [sanitized_to_original[sanitized_names[idx]] for idx in non_matching_indices]
                if len(matching_stations) > 1:
                    narrowed_down_filters.append((''.join(combination), matching_stations))

    elapsed_time = time.time() - start_time
    return narrowed_down_filters, elapsed_time

def read_and_merge_csv(file_paths):
    all_stations_set = set()
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"Warning: The file {file_path} does not exist. Skipping.")
            continue
        df = pd.read_csv(file_path)
        stations = df['Station'].tolist()
        all_stations_set.update(stations)
    return list(all_stations_set)

def combined_filter_finder(file_paths=None, target_stations=None):
    if target_stations is None:
        target_stations = [
            "Bank", "Euston", "Queen's Park", "Stanmore",
            "Swiss Cottage", "Westminster", "White City", "Whitechapel", "Dollis Hill"
        ]

    if file_paths is None:
        file_paths = ["LND_UG.csv"]

    station_names = read_and_merge_csv(file_paths)
    
    sanitized_names, binary_masks, letter_frequencies, sanitized_to_original = preprocess_station_names(station_names)
    
    results = []
    
    for target_station in target_stations:
        best_filters, execution_time_unique = find_best_filters_optimized(sanitized_names, binary_masks, letter_frequencies, target_station_name=target_station)
        narrowed_down_filters, execution_time_narrowed = find_narrowed_down_filters(sanitized_names, binary_masks, target_station_name=target_station, sanitized_to_original=sanitized_to_original)
        
        result = {
            "target_station": target_station,
            "unique_filters": [{"filter": f} for f in best_filters],
            "unique_filters_execution_time": execution_time_unique,
            "narrowed_down_filters": [{"filter": f, "matching_stations": ms} for f, ms in narrowed_down_filters],
            "narrowed_down_filters_execution_time": execution_time_narrowed
        }
        results.append(result)
    
    return json.dumps(results, indent=4)

if __name__ == "__main__":
    print(combined_filter_finder())