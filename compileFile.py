import os
import json

def list_files_in_directory(directory):
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        for idx, filename in enumerate(files, start=1):
            print(f"{idx}. {filename}")
        return files
    except Exception as e:
        print(f"An error occurred while listing files: {e}")
        return []

def compile_json_files(directory, json_files, output_filename):
    combined_data = []
    for filename in json_files:
        file_path = os.path.join(directory, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                combined_data.append(data)
        except Exception as e:
            print(f"Warning: Could not read/parse JSON file '{filename}'. Error: {e}")
    if combined_data:
        home_dir = os.path.expanduser("~")
        downloads_dir = os.path.join(home_dir, "Downloads")
        if not os.path.exists(downloads_dir):
            print(f"Downloads folder not found at {downloads_dir}. Saving to current directory instead.")
            output_path = os.path.join(directory, output_filename)
        else:
            output_path = os.path.join(downloads_dir, output_filename)
        try:
            with open(output_path, 'w', encoding='utf-8') as out_f:
                json.dump(combined_data, out_f, indent=4)
            print(f"\nCombined JSON data saved to: {output_path}")
        except Exception as e:
            print(f"Error writing combined JSON file: {e}")
    else:
        print("\nNo valid JSON files were combined.")

def prompt_user_json_selection(json_files):
    print("\nJSON files available:")
    for idx, filename in enumerate(json_files, start=1):
        print(f"{idx}. {filename}")
    print("\nEnter 'all' to compile all JSON files.")
    selection = input("Enter comma-separated file numbers to compile or 'all': ").strip().lower()
    if selection == 'all':
        return json_files
    else:
        selected_files = []
        try:
            indexes = [int(i.strip()) for i in selection.split(',')]
            for i in indexes:
                if 1 <= i <= len(json_files):
                    selected_files.append(json_files[i-1])
                else:
                    print(f"Warning: {i} is out of valid range.")
            if not selected_files:
                print("No valid file numbers were selected. Exiting.")
                return []
            return selected_files
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas or 'all'. Exiting.")
            return []

if __name__ == "__main__":
    user_input = input("Please enter the directory path: ")
    files = list_files_in_directory(user_input)
    # Filter JSON files only
    json_files = [f for f in files if f.lower().endswith('.json')]
    if not json_files:
        print("\nNo JSON files found in the directory to combine.")
    else:
        selected_files = prompt_user_json_selection(json_files)
        if selected_files:
            output_file = input("Enter the output combined JSON file name (e.g. combined.json): ").strip()
            if not output_file:
                output_file = "combined.json"
            compile_json_files(user_input, selected_files, output_file)
