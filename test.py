import json
import re


def extract_version(version):
    if not version:
        return float('inf')  # Keep records without "browser_version"
    match = re.search(r'\d+\.\d+', version)
    return float(match.group()) if match else 0

def remove_null_values(input_file, output_file):
    # Load the JSON data from the file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Remove keys with null values
    cleaned_data = [{k: v for k, v in record.items() if v is not None} for record in data]

    # Filtering out records which does not support @container css rules
    # https://developer.mozilla.org/en-US/docs/Web/CSS/@container

    # edge >= 105
    filtered_data = [
        record for record in cleaned_data
        if not (record["browser"] == "edge" and extract_version(record["browser_version"]) < 105)
    ]

    # chrome >= 105
    filtered_data = [
        record for record in filtered_data
        if not (record["browser"] == "chrome" and extract_version(record["browser_version"]) < 105)
    ]

    # firefox >= 110
    filtered_data = [
        record for record in filtered_data
        if not (record["browser"] == "firefox" and extract_version(record["browser_version"]) < 110)
    ]

    # opera >= 91
    filtered_data = [
        record for record in filtered_data
        if not (record["browser"] == "opera" and extract_version(record["browser_version"]) < 91)
    ]

    # Save the cleaned data to a new file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, indent=2)

def count_elements(input_file):
    # Load the JSON data from the file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Count the number of elements in the JSON array
    count = len(data)
    print(f'Total number of elements: {count}')

    # Print the first 5 elements
    for i, record in enumerate(data[:5]):
        print(f'Element {i + 1}: {record}')

if __name__ == '__main__':
    # Usage
    input_file = 'browserstack_tests/browsers.json'  # Change to your input filename
    output_file = 'browserstack_tests/browsers_cleaned_3.json'  # Change to your desired output filename

    # remove_null_values(input_file, output_file)
    # print(f'Cleaned JSON saved to {output_file}')
    count_elements(output_file)
