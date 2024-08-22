# txt_to_binary.py
import os
import base64
import string
from pathlib import Path

# Function to sanitize words by removing non-uppercase letters
def sanitize_string(word):
    sanitized = ''.join(char for char in word.upper() if char in string.ascii_uppercase)
    return sanitized

# Function to convert word/phrase into a 26-bit binary mask
def convert_to_binary_mask(word):
    binary_mask = 0
    for char in sanitize_string(word):
        binary_mask |= 1 << (ord(char) - ord('A'))
    return binary_mask

# Generate base64.txt if it doesn't exist
def generate_base64_file(freq_list_file='130k.txt', output_file='base64.txt'):
    if not os.path.exists(output_file):
        binary_rep_list = bytearray()  # Collect all binary representations into a bytearray
        
        # Read the frequency list file and convert each word to its binary mask
        with open(freq_list_file, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                binary_rep = convert_to_binary_mask(word)
                # Convert binary representation to 4-byte (32-bit) format
                binary_rep_list.extend(binary_rep.to_bytes(4, 'big'))
        
        # Encode the entire byte array to Base64 string
        base64_encoded = base64.b64encode(binary_rep_list).decode('utf-8')
        
        # Write the Base64 encoded string to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(base64_encoded)

def load_base64_file(file_path='base64.txt'):
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

def self_test():
    # Ensure base64 file is generated
    generate_base64_file()

    # Load words and their binary representations
    word_list, binary_word_map = load_base64_file()

    # List the first 10 words and their binary representations
    print("First 10 words and their bitmasks:")
    max_length = max(len(word) for word in word_list[:10])
    for word in word_list[:10]:
        padded_word = word.ljust(max_length)
        bitmask = bin(binary_word_map[word])[2:].zfill(32)
        print(f"{padded_word}\t{bitmask}")

    # Define the filter and constraints
    filter_mask = convert_to_binary_mask("ANORT")
    constraint_mask = convert_to_binary_mask("CHIGWEL")
    
    # Find the first 5 words matching the filter and not containing any constraint letters
    matching_words = []
    for word in word_list:
        bitmask = binary_word_map[word]
        if (bitmask & filter_mask == filter_mask) and (bitmask & constraint_mask == 0):
            matching_words.append(word)
            if len(matching_words) == 5:
                break
    
    print("\nFirst 5 words that match the filter 'ANORT' and do not contain letters in 'CHIGWEL':")
    for word in matching_words:
        print(word)

def main():
    # Check and generate base64 file if it doesn't exist
    if not Path('base64.txt').exists():
        generate_base64_file()
    
    # Run the self-test
    self_test()

if __name__ == "__main__":
    main()