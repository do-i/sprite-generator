import json

# Step 1: Define the Node model
class Node:
    def __init__(self, type_name, name):
        self.type_name = type_name
        self.name = name
        self.nodes = []

    def __repr__(self):
        return f"Node(type={self.type_name}, name={self.name}, children={len(self.nodes)})"

# Step 2: Create base instances in a lookup dict
base_frames = ['child', 'female', 'male', 'muscular', 'pregnant', 'teen']
quick_dict = {frame: Node("base_frame", frame) for frame in base_frames}

def log_standalone_items(metadata_dict):
    print("--- Standalone Items (No Requirements) ---")
    standalone_count = 0

    # Sort by category to make the log readable
    for t_name in sorted(metadata_dict.keys()):
        items = metadata_dict[t_name]

        # Filter for items where the 'required' list is empty
        universal_items = [i['name'] for i in items if not i.get('required')]

        if universal_items:
            print(f"\nCategory: [{t_name}]")
            for name in sorted(set(universal_items)):
                print(f"  - {name}")
                standalone_count += 1

    print(f"\nTotal Standalone Items Found: {standalone_count}")


def print_dependency_graph(metadata_dict):
    dependencies = {}

    for t_name, items in metadata_dict.items():
        # Collect all unique requirements for this category
        all_reqs = set()
        for item in items:
            for req in item.get('required', []):
                all_reqs.add(req)

        dependencies[t_name] = sorted(list(all_reqs))

    print("--- Sprite Dependency Graph ---")
    for category, reqs in sorted(dependencies.items()):
        if not reqs:
            print(f" {category} (Standalone)")
        else:
            # Format: Category -> [Req1, Req2]
            req_str = ", ".join(reqs)
            print(f" {category} ──► Requires: [{req_str}]")


# Assuming your pure JSON is an object/dict
with open('item-metadata.json', 'r') as f:
    items = json.load(f)

type_to_objects = {}

# Iterate over values since 'items' is a dict
for item in items.values():
    t_name = item.get('type_name')
    name = item.get('name')

    # Default to an empty list if 'variants' is missing
    variants = item.get('variants', [])
    required = item.get('required', [])

    if t_name and name:
        if t_name not in type_to_objects:
            type_to_objects[t_name] = []
        obj = {
            "name": name,
            "variants": variants,
            "required": required
        }
        # Ensure we don't add the exact same object twice
        if obj not in type_to_objects[t_name]:
            type_to_objects[t_name].append(obj)

metadata_dict = type_to_objects

# Execute
# print_dependency_graph(metadata_dict)

# Execute the check
# log_standalone_items(metadata_dict)

# Verify

print(f"Initialized base_frames: {quick_dict}")