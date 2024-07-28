import json

input_file = 'pak_city_names.json'
output_file = 'pak_city_names.json'

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as infile:
        return json.load(infile)

def write_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)

def extract_names(data):
    return [{"name": item["name"]} for item in data]

# Function to add new entries
def add_entries():
    entries = []
    while True:
        name = input("Enter name (or type 'done' to finish): ")
        if name.lower() == 'done':
            break
        entries.append({"name": name})
    return entries

data = read_json(input_file)

names = extract_names(data)

# Add new entries
new_entries = add_entries()
names.extend(new_entries)

write_json(output_file, names)

print(f"Updated names have been written to {output_file}")
