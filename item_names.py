import csv
import json

def load_metadata_to_dict():

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
  return type_to_objects

def export_unique_csv(metadata_dict, filename="item_metadata_list.csv"):
    # Using a set of tuples to ensure (type, name) pairs are unique
    unique_pairs = set()

    for type_name, items in metadata_dict.items():
        for item in items:
            name = item.get('name')
            if name:
                unique_pairs.add((type_name, name))

    # Sort by type_name first, then name
    sorted_pairs = sorted(list(unique_pairs))

    with open(filename, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["type_name", "name"])  # Header
        writer.writerows(sorted_pairs)

    print(f"Success: {len(sorted_pairs)} unique items saved to {filename}")


# Execute
export_unique_csv(load_metadata_to_dict())