import chardet

# Detect encoding
def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read(10000)  # Read a portion of the file
        result = chardet.detect(raw_data)
    return result['encoding']

# Define the input and output file names
input_file = r'adblock.txt'
output_file = r'adblock_cleaned.txt'

def remove_duplicate_urls(input_file, output_file):
    try:
        # Open the input file and read lines with utf-8 encoding
        with open(input_file, 'r', encoding='utf-8', errors='replace') as file:
            lines = file.readlines()
        
        # Use a set to remove duplicate lines
        unique_lines = set(lines)
        
        # Open the output file and write the unique lines with utf-8 encoding
        with open(output_file, 'w', encoding='utf-8') as file:
            file.writelines(sorted(unique_lines))  # Sorting is optional
        
        print(f"Removed duplicates and saved the result to {output_file}")
    
    except FileNotFoundError:
        print(f"Error: The file {input_file} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function
remove_duplicate_urls(input_file, output_file)