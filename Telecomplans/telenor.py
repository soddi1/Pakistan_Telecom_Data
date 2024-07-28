import json
import os
import re

def extract_duration(details_list):
    duration_keywords = {
        "monthly": "Monthly",
        "yearly": "Yearly",
        "daily": "Daily",
        "day": "Daily",
        "weekly": "Weekly"
    }
    
    for detail in details_list:
        detail_lower = detail.lower()
        # Check for known keywords first
        for keyword, duration in duration_keywords.items():
            if keyword in detail_lower:
                print(f"Keyword '{keyword}' found in detail: '{detail}'. Setting duration to '{duration}'")
                return duration
        
        # Check for numerical patterns like "15 days", "3 weeks"
        match_days = re.search(r'(\d+)\s*days?', detail_lower, re.IGNORECASE)
        match_weeks = re.search(r'(\d+)\s*weeks?', detail_lower, re.IGNORECASE)
        match_months = re.search(r'(\d+)\s*months?', detail_lower, re.IGNORECASE)
        match_years = re.search(r'(\d+)\s*years?', detail_lower, re.IGNORECASE)
        
        if match_days:
            duration = f"{match_days.group(1)} Days"
            print(f"Pattern '{match_days.group(0)}' found in detail: '{detail}'. Setting duration to '{duration}'")
            return duration
        if match_weeks:
            duration = f"{match_weeks.group(1)} Weeks"
            print(f"Pattern '{match_weeks.group(0)}' found in detail: '{detail}'. Setting duration to '{duration}'")
            return duration
        if match_months:
            duration = f"{match_months.group(1)} Months"
            print(f"Pattern '{match_months.group(0)}' found in detail: '{detail}'. Setting duration to '{duration}'")
            return duration
        if match_years:
            duration = f"{match_years.group(1)} Years"
            print(f"Pattern '{match_years.group(0)}' found in detail: '{detail}'. Setting duration to '{duration}'")
            return duration
    
    print(f"No duration keyword or pattern found in details: '{details_list}'")
    return None

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
    
    output_data = []
    
    for plan in input_data.get("Price_plans", []):
        for sub in plan.get("Subs", []):
            for name_item in sub.get("Name", []):
                filtered_details = [detail.get("Details", "") for detail in name_item.get("Details", [])]
                
                duration = extract_duration(filtered_details)
                
                new_item = {
                    "name": name_item.get("name", "N/A"),
                    "Price": name_item.get("Price", "N/A"),
                    "Duration": duration,
                    "Details": filtered_details
                }
                
                output_data.append(new_item)
    
    try:
        with open(output_filename, 'w') as outfile:
            json.dump(output_data, outfile, indent=4)
        print(f"Successfully written to {output_filename}")
    except IOError as e:
        print(f"Error writing to {output_filename}: {e}")

# Example usage
input_filename = 'c:/Users/Dell/Desktop/A_Project/Flooding/OpenCelliD data/Flooding/PTA-Data-Analysis/Telecomplans/telenor.json'
output_filename = 'c:/Users/Dell/Desktop/A_Project/Flooding/OpenCelliD data/Flooding/PTA-Data-Analysis/Telecomplans/telenor_processed.json'
convert_json(input_filename, output_filename)
