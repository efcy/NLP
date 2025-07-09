import os
import json
from pathlib import Path

def parse_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Initialize variables to store parsed data
    parsed_data = {
        'title': None,
        'title_translation': None,
        'date': None,
        'author': None,
        'url': None,
        'text': None,
        'origin': None,
        'translation': None,
    }
    
    # Split the file into lines and parse key-value pairs
    lines = content.split('\n')
    current_key = None
    current_value = []
    
    for line in lines:
        if line.startswith(('title:', 'title_translation:', 'date:', 'author:', 'url:', 'text:', 'origin:', 'translation:')):
            # Save the previous key-value pair if exists
            if current_key:
                parsed_data[current_key] = '\n'.join(current_value).strip()
            
            # Start new key-value pair
            current_key = line.split(':', 1)[0].strip()
            current_value = [line.split(':', 1)[1].strip()]
        else:
            if current_key:  # Continue appending to the current value
                current_value.append(line.strip())
    
    # Save the last key-value pair
    if current_key:
        parsed_data[current_key] = '\n'.join(current_value).strip()
    
    return parsed_data

def process_folder(input_folders, output_file):
    all_data = []
    for input_folder in input_folders:
        for filename in os.listdir(input_folder):
            file_path = os.path.join(input_folder, filename)
            if os.path.isfile(file_path):
                parsed_data = parse_file(file_path)
                all_data.append(parsed_data)
        
    # Save to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    
    print(f"Processed {len(all_data)} files. Output saved to {output_file}.")

# Example usage
input_folder = ['data/guardian', 'data/chinese']  # Replace with your folder path
output_file = 'output.json'
process_folder(input_folder, output_file)