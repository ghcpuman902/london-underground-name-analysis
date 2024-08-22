# 🚇 London Underground Name Fun Project: A Journey Through the Alphabet

[👋 Hello, Threads Community!](https://www.threads.net/@bowlofchalk/post/C-hKosIopxE) 🎉

Welcome to a quirky and fun exploration of London Underground station names! If you’ve ever pondered the oddities of station name letters—or found yourself wondering about *MACKEREL*—you’re in for a treat. Spoiler alert: **St John's Wood** is the only station on the Tube without any letters from *MACKEREL*. But there’s so much more to uncover!

## 🔍 What’s in a Name?

This project is all about discovering fascinating patterns in the letters of station names. Here’s what we found:

### 🔥 Heatmaps

- **🅰️ Alphabetical Insight:**
  Ever wondered which letters pop up most often in London Underground stations? This heatmap sorts all station names alphabetically, giving a clear picture of letter frequency.

  ![Alphabetically Sorted Heatmap](london_underground_station_heatmap_alphabetical.png)

- **📈 Frequency Insight:**
  Here, station names are sorted by how often each letter appears, grouping stations with the most common letters together. **St John's Wood** stands out as the fifth from the bottom—a fun twist in the world of Tube stations.

  ![Frequency Sorted Heatmap](london_underground_station_heatmap_frequency.png)

- **🔠 Unique Letters Insight:**
  What about those stations with rare letters? This heatmap flips the frequency order, putting the stations with the rarest letters (like `Z` and `J`) at the top.

  ![Reverse Frequency Sorted Heatmap](london_underground_station_heatmap_reverse_frequency.png)

## 🎉 Fun Facts

- **St John's Wood**: The only station without any letters from *MACKEREL*.
- **Pimlico** & **Dollis Hill**: No `E`, `R`, `A`, or `N` in their names.
- **Belsize Park**: The only station with a `Z`.
- **St James Park**, **Willesden Junction**, & **St John's Wood**: The only stations with a `J`.

### 📝 Letter Frequency in Station Names
`E`, `R`, `A`, `N`, `O`, `T`, `S`, `L`, `I`, `H`, `D`, `W`, `G`, `C`, `U`, `B`, `M`, `P`, `K`, `Y`, `F`, `V`, `Q`, `X`, `J`, `Z`

---

## 🧩 Finding the Best Letter Filters

We've developed tools to help find the most interesting letter filters for London Underground station names.

### `txt_to_binary.py`

1. **What it does:**
   - Reads an ordered list of words/phrases from `130k.txt`.
   - Converts each word/phrase into a 26-bit binary representation (one bit per letter of the English alphabet).
   - Encodes these binary masks into a Base64 format.
   - Outputs a single concatenated Base64 string into `base64.txt`.

2. **How to run it:**
   ```bash
   python txt_to_binary.py
   ```
   This will generate `base64.txt` which contains the Base64 encoded binary representation of each word in `130k.txt`.

### `find_words.py`

1. **What it does:**
   - Loads the Base64 encoded data from `base64.txt` (if it doesn't exist, it prompts you to run `txt_to_binary.py`).
   - Runs `combined_filter_finder` to get unique and narrowed-down filters for specified target stations.
   - Finds the top 2 (configurable) most frequent words that match these filters.
   - Appends these words to the original JSON data and outputs the result.

2. **How to run it:**
   ```bash
   python find_words.py
   ```
   This generates a `final_output.json` file that includes the top words for each filter, helping to create new puzzles or insights.

### Testing and Running

For testing and running the analysis:
1. **Edit `test.py`:**
   - Adjust the `target_stations` variable to the stations you want to analyze.
   - Run the following command to test and find the best filter for each station:
   ```bash
   python test.py
   ```

2. **Run `find_words.py`** to generate the best words from the given station names to make a new puzzle:
   ```bash
   python find_words.py
   ```

---

Thanks for joining the fun! If you're curious to see more or just want to chat about it, don’t forget to check out the original [Threads post](https://www.threads.net/@bowlofchalk/post/C-hKosIopxE)!