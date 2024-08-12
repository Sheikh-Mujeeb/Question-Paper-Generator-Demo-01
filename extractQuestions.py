import json

def extract_json_from_text(text):
    # Initialize variables to track the start and end of JSON content
    start_index = None
    open_brackets = 0
    
    # Traverse each character in the text
    for i, char in enumerate(text):
        if char == '[':
            if start_index is None:
                start_index = i  # Mark the start of JSON
            open_brackets += 1
        elif char == ']':
            open_brackets -= 1
            if open_brackets == 0 and start_index is not None:
                # Complete JSON found
                try:
                    # Extract the substring and parse it as JSON
                    json_str = text[start_index:i+1]
                    return json.loads(json_str)
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON: {e}")
                    return None
    return None