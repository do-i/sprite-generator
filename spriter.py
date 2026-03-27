import re
import json

def load_metadata(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    # Regex to find the array assigned to the 'items' variable
    match = re.search(r'=\s*(\[[\s\S]*\]);', content)
    return json.loads(match.group(1))

items = load_metadata('item-metadata.js')
type_to_names = {}

for item in items:
    t_name = item.get('type_name')
    name = item.get('name')

    if t_name and name:
        # If the key doesn't exist, set it to an empty list first
        if t_name not in type_to_names:
            type_to_names[t_name] = []

        # Now append safely (ensures the first name is actually added)
        if name not in type_to_names[t_name]:
            type_to_names[t_name].append(name)

# Step 2: Verify
print(f"Verified 'body' keys: {type_to_names.get('body', [])[:5]}")