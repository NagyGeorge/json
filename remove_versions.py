#!/usr/bin/env python3
import json
import sys
import argparse
import re

def remove_versions_from_json(input_file, output_file):
    """
    Remove 'version' fields from JSON objects and save to a new file.
    
    Args:
        input_file (str): Path to the input JSON file
        output_file (str): Path to the output JSON file
    """
    try:
        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # The file contains JSON objects separated by commas but not wrapped in an array
        # We need to wrap it in brackets to make it valid JSON
        if not content.startswith('['):
            content = '[' + content + ']'
        
        # Remove trailing commas before closing brackets
        content = re.sub(r',(\s*\])', r'\1', content)
        
        # Parse the JSON
        data = json.loads(content)
        
        # Process the data to remove version fields
        if isinstance(data, list):
            # If it's a list of objects, remove version from each object
            cleaned_data = []
            for item in data:
                if isinstance(item, dict):
                    # Create a new dict without the 'version' key
                    cleaned_item = {k: v for k, v in item.items() if k != 'version'}
                    cleaned_data.append(cleaned_item)
                else:
                    cleaned_data.append(item)
        elif isinstance(data, dict):
            # If it's a single object, remove version field
            cleaned_data = {k: v for k, v in data.items() if k != 'version'}
        else:
            # If it's neither list nor dict, keep as is
            cleaned_data = data
        
        # Write the cleaned data to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(cleaned_data, f, indent='\t', ensure_ascii=False)
        
        print(f"Successfully processed {input_file}")
        print(f"Output saved to {output_file}")
        print(f"Removed version fields from {len(cleaned_data) if isinstance(cleaned_data, list) else 1} item(s)")
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file '{input_file}': {e}")
        print("Debug info:")
        print(f"Content preview: {content[:200]}...")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Remove 'version' fields from JSON objects",
        epilog="Example: python script.py input.json output.json"
    )
    parser.add_argument('input_file', help='Input JSON file path')
    parser.add_argument('output_file', help='Output JSON file path')
    
    args = parser.parse_args()
    
    remove_versions_from_json(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
