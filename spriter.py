import json

# Assuming your pure JSON is an object/dict
with open('item-metadata.json', 'r') as f:
    items = json.load(f)

type_to_names = {}

# Iterate over values since 'items' is a dict
for item in items.values():
    t_name = item.get('type_name')
    name = item.get('name')

    if t_name and name:
        if t_name not in type_to_names:
            type_to_names[t_name] = []

        if name not in type_to_names[t_name]:
            type_to_names[t_name].append(name)

# Step 2: Verify
print(f"Categories found: {list(type_to_names.keys())}")
print(f"Body names: {type_to_names.get('body', [])[:5]}")