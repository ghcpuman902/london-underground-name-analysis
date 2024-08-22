# test.py

import unique_filter_finder
import combined_filter_finder
import conditional_filter_stations

def test_external_scripts():
    target_stations = [
            "Bank", "Euston", "Queen's Park", "Stanmore",
            "Swiss Cottage", "Westminster", "White City", "Whitechapel", "Dollis Hill"
            ]
    file_paths = ["LND_UG.csv"]

    # Test conditions for conditional_filter_stations
    test_conditions = [
        {"condition": "JZ", "include": True, "any_or_all": 'any'},
        {"condition": "AEIOU", "include": True, "any_or_all": 'all'},
        {"condition": "NEAR", "include": False}
    ]
    
    for test_case in test_conditions:
        condition = test_case["condition"]
        include = test_case["include"]
        any_or_all = test_case.get("any_or_all", 'any')
        result = conditional_filter_stations.conditional_filter_stations(file_paths=file_paths, condition=condition, include=include, any_or_all=any_or_all)
        print(f"Condition: {condition}, Include: {include}, Any or All: {any_or_all}")
        print(result)
        print()

    # Test unique_filter_finder
    unique_result = unique_filter_finder.unique_filter_finder(file_paths=file_paths, target_stations=target_stations)
    print("Unique Filter Finder Result:\n", unique_result)
    
    # Test combined_filter_finder
    combined_result = combined_filter_finder.combined_filter_finder(file_paths=file_paths, target_stations=target_stations)
    print("Combined Filter Finder Result:\n", combined_result)

if __name__ == "__main__":
    test_external_scripts()