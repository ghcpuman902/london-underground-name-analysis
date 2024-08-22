# 🚇 London Underground Name Fun Project: A Journey Through the Alphabet

[👋 Hello, Threads Community!](https://www.threads.net/@bowlofchalk/post/C-hKosIopxE) 🎉

Welcome to a quirky and fun exploration of London Underground station names! If you've ever pondered the oddities of station name letters—or wondered about *MACKEREL*—you're in for a treat. Spoiler alert: **St John's Wood** is the only station on the Tube without any letters from *MACKEREL*. But there's so much more to uncover!

## 🔎 Station Name Collage

This project is about discovering fascinating patterns in the letters of station names. Here's what we found:

## 🎉 Fun Facts

- **St John's Wood**: The only station without any letters from *MACKEREL*. But *REALLY* any word with the letters "ERAL" but without "ST JOHNWD" would work, like *REAL*.
- **Pimlico** & **Dollis Hill**: *NEAR* is enough to narrow down to only these two. Individually, Pimlico can be narrowed down with *RESTAURANT* and Dollis Hill with *ENTRANCE*.
- **Belsize Park**: The only station with a `Z`.
- **St James Park**, **Willesden Junction**, & **St John's Wood**: The only stations with a `J`.
- **Chigwell**: *TRANSPORT*
- **Bank**: *SHORT LIVED*
- **Amersham**: *CITY OF LONDON*

### 🅰️ Alphabet Heatmaps

- **Most Common Letters on Top:**
  Check out this heatmap to understand why *MACKEREL* works as a filter for **St John’s Wood**—station names are sorted by how often each letter appears, grouping stations with the most common letters together.

  ![Frequency Sorted Heatmap](london_underground_station_heatmap_frequency.png)

- **Rare Letters On Top:**
  This heatmap shows stations with rare letters (like `Z` and `J`), putting them at the top.

  ![Reverse Frequency Sorted Heatmap](london_underground_station_heatmap_reverse_frequency.png)

- **Alphabetic Order:**

  ![Alphabetically Sorted Heatmap](london_underground_station_heatmap_alphabetical.png)

### 📝 Letter Frequency in Station Names
`E`, `R`, `A`, `N`, `O`, `T`, `S`, `L`, `I`, `H`, `D`, `W`, `G`, `C`, `U`, `B`, `M`, `P`, `K`, `Y`, `F`, `V`, `Q`, `X`, `J`, `Z`

---

## 🚀 Getting Started

### Step-by-Step Guide:
1. **Clone the Repository**
   ```bash
   git clone https://github.com/ghcpuman902/london-underground-name-analysis.git
   cd london-underground-name-analysis
   ```
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Analysis**
   ```bash
   python test.py
   ```
4. **See the Magic**
   Check the output to discover unique and interesting patterns in station names!

## 🧩 Finding the Best Letter Filters

I have developed tools to help find the most interesting letter filters for London Underground station names.

This is accomplished using a highly efficient Python version, and there's also [an interactive web version](https://manglekuo.com/works/london-underground-name-analysis/name-lab).

A lot of effort went into making this extremely fast, with valuable assistance from ChatGPT. The main idea is to avoid unnecessary searches and use a binary bitmask to speed up the comparison.

### Running

1. **Use `test.py` if you are only interested in the best filter for each station:**
   - Edit the file to adjust the `target_stations` variable to the stations you want to analyse.
   - Run the following command to test and find the best filters for each station:
   ```zsh
   python test.py
   ```
   - This will provide filters for the target station name. These filters are letter combinations that **do not** share any letters with the target station name but share at least one letter with all other stations.
   - Additionally, it will output "narrowed down filters," which are letter combinations that narrow down the possibilities to a small group of stations, including the target station. By default, we are particularly interested in filters that are shorter than 4 letters and reduce the group size to less than 5 stations.

2. **Use `find_words.py` if you want to make your own puzzle:**
   - Edit the file to adjust the `target_stations` variable to the stations you want to analyse.
   - Run the following command to test and find the best filters and their corresponding English words for each station:
   ```zsh
   python find_words.py
   ```
   - This will run `combined_filter_finder` to get unique and narrowed-down filters for specified target stations.
   - Find the top 2 (configurable) most frequently used English words or phrases that match these filters.
   - Output the result as `final_output.json`.

### How does it work?

### `combined_filter_finder.py`

1. **What it does:**
   - Preprocesses the station names by sanitising and counting the frequency of each letter across all station names.
   - Converts each station name into a 26-bit binary representation, where each bit corresponds to an English alphabet letter's presence.
   - Utilises precomputed letter frequencies to prioritise and propose filters from the most probable to the least.
   - Tests each filter for both unique and narrowed-down criteria, recording and outputting the results.

2. **How to run:**
   - Edit the file to adjust the `target_stations` variable to the stations you want to analyse.
   ```zsh
   python combined_filter_finder.py
   ```

### `txt_to_binary.py`

1. **What it does:**
   - Reads an ordered list of words/phrases from `130k.txt`.
   - Converts each word/phrase into a 26-bit binary representation (one bit per English alphabet letter).
   - Encodes these binary masks into a Base64 format.
   - Outputs a single concatenated Base64 string into `base64.txt`, ensuring a super fast look-up in our `find_words.py` script.

2. **How to run:**
   ```zsh
   python txt_to_binary.py
   ```
   This will generate `base64.txt`, which contains the Base64-encoded binary representation of each word in `130k.txt`.

### `find_words.py`

1. **What it does:**
   - Loads the Base64 encoded data from `base64.txt` (if it doesn't exist, it prompts you to run `txt_to_binary.py`).
   - Runs `combined_filter_finder` to get unique and narrowed-down filters for specified target stations.
   - Finds the top 2 (configurable) most frequent words that match these filters.
   - Appends these words to the original JSON data and outputs the result.

2. **How to run:**
   ```zsh
   python find_words.py
   ```
   This generates a `final_output.json` file that includes the top words for each filter, helping to create new puzzles or insights.

### `conditional_filter_stations.py`

1. **What it does:**
   - Filters stations based on a given set of conditions.
   - Includes two filtering methods: 
     - Lists stations with names containing any or all of the specified letters.
     - Lists stations with names excluding any of the specified letters.

2. **How to run:**
   ```zsh
   python conditional_filter_stations.py
   ```
   Run with varied conditions to filter stations either by including or excluding specific letters.

### `test.py`

1. **What it does:**
   - Runs both `unique_filter_finder` and `combined_filter_finder`, `unique_filter_finder` only looks for unique filters.
   - A filter is a combination of letters that **does not** share any letters with the target station name but shares at least one with all other stations.
   - For example, for Bank it is "ELOR", meaning all other station names except for Bank have "E", "L", "O", "R". So, a word containing these 4 letters but no letters from "Bank" would make a good Mackerel puzzle.
   - Sometimes, if we can't find such a filter, we are interested in a filter that can at least narrow down to a small group. For example, a filter that narrows it down to a group of 2-3 stations.

   ```zsh
   python find_words.py
   ```

## 📚 Conclusion

Explore the quirky and fun world of London Underground station names with this project. Whether you're interested in finding unique letter patterns, creating your own word puzzles, or just learning more about the fascinating names of the Tube stations, there's something here for everyone. Dive in, and discover a new way to look at the London Underground!

Happy exploring! 🎉🚇