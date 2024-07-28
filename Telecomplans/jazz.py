import json
import os

def convert_json(input_filename, output_filename):
    if not os.path.isfile(input_filename):
        print(f"Error: The file {input_filename} does not exist.")
        return
    
    try:
        with open(input_filename, 'r') as infile:
            input_data = json.load(infile)
    except json.JSONDecodeError as e:
        print(f"Error reading JSON from {input_filename}: {e}")
        return
    
    output_data = {
        "Jazz": []
    }
    
    valid_durations = ["Yearly", "Monthly", "Weekly", "Daily"]
    
    for item in input_data.get("Jazz", []):
        filtered_details = [detail.get("Details", "") for detail in item.get("Details", [])]
        
        duration = item.get("Type", None)
        if duration not in valid_durations:
            duration = None
        
        new_item = {
            "name": item.get("name", "N/A"),
            "Duration": duration,
            "Price": item.get("Price", "N/A"),
            "Details": filtered_details
        }
        
        output_data["Jazz"].append(new_item)
    
    try:
        with open(output_filename, 'w') as outfile:
            json.dump(output_data, outfile, indent=4)
        print(f"Successfully written to {output_filename}")
    except IOError as e:
        print(f"Error writing to {output_filename}: {e}")

# Example usage
input_filename = 'c:/Users/Dell/Desktop/A_Project/Flooding/OpenCelliD data/Flooding/PTA-Data-Analysis/Telecomplans/jazz.json'
output_filename = 'c:/Users/Dell/Desktop/A_Project/Flooding/OpenCelliD data/Flooding/PTA-Data-Analysis/Telecomplans/jazz_processed.json'
convert_json(input_filename, output_filename)
