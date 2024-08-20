import chardet
import os

# Detect encoding
def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read(10000)  # Read a portion of the file
        result = chardet.detect(raw_data)
    return result['encoding']

# Define the input file and output file prefix
input_file = r'master_adblock_list.txt'
output_file_prefix = r'master_adblock_list_new'
max_file_size_mb = 24
max_file_size_bytes = max_file_size_mb * 1024 * 1024  # Convert MB to bytes


def remove_duplicate_urls(input_file, output_file_prefix):
    try:
        # Open the input file and read lines with utf-8 encoding
        with open(input_file, 'r', encoding='utf-8', errors='replace') as file:
            lines = file.readlines()
        
        # Use a set to remove duplicate lines
        unique_lines = set(lines)
        
        # Prepare to write the output in chunks
        file_number = 1
        current_file_size = 0
        
        # Start writing to the first output file
        output_file = f"{output_file_prefix}_{file_number}.txt"
        with open(output_file, 'w', encoding='utf-8') as file:
            for line in sorted(unique_lines):
                line_length = len(line.encode('utf-8'))  # Get the size of the line in bytes
                if current_file_size + line_length > max_file_size_bytes:
                    # Close the current file and start a new one
                    file.close()
                    print(f"Saved {output_file} ({current_file_size / 1024 / 1024:.2f} MB)")
                    file_number += 1
                    current_file_size = 0
                    output_file = f"{output_file_prefix}_{file_number}.txt"
                    file = open(output_file, 'w', encoding='utf-8')
                
                file.write(line)
                current_file_size += line_length
        
        # Close the last file
        file.close()
        print(f"Saved {output_file} ({current_file_size / 1024 / 1024:.2f} MB)")
    
    except FileNotFoundError:
        print(f"Error: The file {input_file} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function
remove_duplicate_urls(input_file, output_file_prefix)