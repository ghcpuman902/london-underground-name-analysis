# test.py

import unique_filter_finder
import combined_filter_finder

def test_external_scripts():
    target_stations = [
            "Bank", "Euston", "Queen's Park", "Stanmore",
            "Swiss Cottage", "Westminster", "White City", "Whitechapel", "Dollis Hill"
            ]
    file_paths = ["LND_UG.csv"]

    # Test unique_filter_finder
    unique_result = unique_filter_finder.unique_filter_finder(file_paths=file_paths, target_stations=target_stations)
    print("Unique Filter Finder Result:\n", unique_result)
    
    # Test combined_filter_finder
    combined_result = combined_filter_finder.combined_filter_finder(file_paths=file_paths, target_stations=target_stations)
    print("Combined Filter Finder Result:\n", combined_result)

if __name__ == "__main__":
    test_external_scripts()