import json


def remove_null_values(input_file, output_file):
    # Load the JSON data from the file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Remove keys with null values
    cleaned_data = [{k: v for k, v in record.items() if v is not None} for record in data]

    # Save the cleaned data to a new file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=2)


if __name__ == '__main__':
    # Usage
    input_file = 'browserstack_tests/browsers.json'  # Change to your input filename
    output_file = 'browserstack_tests/browsers_cleaned.json'  # Change to your desired output filename
    remove_null_values(input_file, output_file)
    print(f'Cleaned JSON saved to {output_file}')