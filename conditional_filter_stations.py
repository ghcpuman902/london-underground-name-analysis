# conditional_filter_stations.py

import json
import os
import pandas as pd
import string

def sanitize_station_name(station_name):
    sanitized = ''.join([char for char in station_name.upper() if char in string.ascii_uppercase])
    return sanitized

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

def filter_stations_include(stations, condition, any_or_all='any'):
    condition_set = set(condition.upper())
    
    if any_or_all == 'all':
        filtered_stations = [
            station for station in stations 
            if condition_set.issubset(sanitize_station_name(station))
        ]
    else:
        filtered_stations = [
            station for station in stations 
            if condition_set.intersection(sanitize_station_name(station))
        ]
    
    return filtered_stations

def filter_stations_exclude(stations, condition):
    condition_set = set(condition.upper())
    filtered_stations = [station for station in stations if not condition_set.intersection(sanitize_station_name(station))]
    return filtered_stations

def conditional_filter_stations(file_paths=None, condition="NEAR", include=True, any_or_all='any'):
    if file_paths is None:
        file_paths = ["LND_UG.csv"]

    station_names = read_and_merge_csv(file_paths)
    
    if include:
        filtered_stations = filter_stations_include(station_names, condition, any_or_all)
    else:
        filtered_stations = filter_stations_exclude(station_names, condition)
    
    return json.dumps(filtered_stations, indent=4)

if __name__ == "__main__":
    # Example usage:
    test_conditions = [
        {"condition": "JZ", "include": True, "any_or_all": 'any'},
        {"condition": "AEIOU", "include": True, "any_or_all": 'all'},
        {"condition": "NEAR", "include": False}
    ]

    for test_case in test_conditions:
        condition = test_case["condition"]
        include = test_case["include"]
        any_or_all = test_case.get("any_or_all", 'any')
        result = conditional_filter_stations(condition=condition, include=include, any_or_all=any_or_all)
        print(f"Condition: {condition}, Include: {include}, Any or All: {any_or_all}")
        print(result)
        print()