import random
import pandas as pd
import json

# 1. Update Node Model to include classification
class Node:
    def __init__(self, type_name, name, classification="Universal"):
        self.type_name = type_name
        self.name = name
        self.classification = classification
        self.nodes = []

    def __repr__(self):
        return f"[{self.classification}] {self.type_name}: {self.name}"


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


# 3. The Generator Function
def generate_sprite(base_frame, mode="Humanoid"):
    """
    mode: "Humanoid" or "Non-Humanoid"
    """
    root = quick_dict.get(base_frame)
    if not root: return "Invalid base frame"

    # Pool items by category and classification
    # 'Universal' items are always included in the pool
    allowed_classes = [mode, "Universal"]
    pool = {}
    for node in root.nodes:
        if node.classification in allowed_classes:
            pool.setdefault(node.type_name, []).append(node)

    selected_items = []

    # Guardrail 1: Mandatory Categories
    mandatory = ['body', 'head', 'hair', 'torso', 'legs']
    for cat in mandatory:
        if cat in pool:
            selected_items.append(random.choice(pool[cat]))

    # Guardrail 2: Optional Items (2 to 5)
    # Filter out categories already used in mandatory
    remaining_cats = [c for c in pool.keys() if c not in mandatory]
    num_optional = random.randint(2, 5)

    # Randomly pick unique categories for optional items
    extra_cats = random.sample(remaining_cats, min(len(remaining_cats), num_optional))
    for cat in extra_cats:
        selected_items.append(random.choice(pool[cat]))

    return selected_items


class_df = pd.read_csv('classified_items.csv')
class_map = {(row['type_name'], row['name']): row['classification'] for _, row in class_df.iterrows()}
metadata_dict = load_metadata_to_dict()

base_frames = ['child', 'female', 'male', 'muscular', 'pregnant', 'teen']
quick_dict = {frame: Node("base_frame", frame) for frame in base_frames}

# Re-link logic with classification
for type_name, items in metadata_dict.items():
    for item in items:
        name = item.get('name')
        reqs = item.get('required', [])
        classification = class_map.get((type_name, name), "Universal")

        item_node = Node(type_name, name, classification)
        for req in reqs:
            if req in quick_dict:
                quick_dict[req].nodes.append(item_node)


# --- Example Usage ---
print("--- Randomized Enemy (Non-Humanoid) ---")
enemy = generate_sprite("male", mode="Non-Humanoid")
for item in enemy:
    print(item)