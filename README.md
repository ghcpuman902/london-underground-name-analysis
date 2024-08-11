# London Underground Name Analysis

**London Underground Name Analysis** is a data visualisation project that generates and analyses heatmaps of London Underground station names. These heatmaps highlight the presence of each letter (A-Z) within the station names, offering unique insights into letter distribution across the Tube network.

## Heatmap Visualisations

### Alphabetical Insight
This heatmap displays station names sorted alphabetically, revealing patterns in letter usage across the Tube network.

![Alphabetically Sorted Heatmap](london_underground_station_heatmap_alphabetical.png)

### Frequency Insight
This heatmap sorts station names by the frequency of letters, clustering stations with the most common letters together.

![Frequency Sorted Heatmap](london_underground_station_heatmap_frequency.png)

## How to Use

To generate these visualisations yourself, simply run the provided Python script `generate_heatmaps.py` with the station data (`LND_UG.csv`). The script will output two heatmaps as shown above.

### Run the Script
```bash
python generate_heatmaps.py