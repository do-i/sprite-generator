import random
import pandas as pd
import json

SPRITE_GEN_URL = "http://localhost:8000" # Start service with `python -m http.server 8000`
# SPRITE_GEN_URL = "https://liberatedpixelcup.github.io/Universal-LPC-Spritesheet-Character-Generator/"

# 1. Update Node Model to include classification
class Node:
    def __init__(self, type_name, name, classification="Universal", variants=[]):
        self.type_name = type_name
        self.name = name
        self.classification = classification
        self.variant_list = variants
        self.variant = ''
        self.nodes = []

    def __repr__(self):
        return {
            'type_name': self.type_name,
            'name': self.resolved_name,
            'variant': self.variant
          }

    def url_param_format(self):
        resolved_name = self.name.replace(' ', '_')
        return f"{self.type_name}={resolved_name}_{self.variant}"



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


def generate_sprite(base_frame, mode, seed=None):
    rng = random.Random(seed)   # isolated deterministic RNG

    root = quick_dict.get(base_frame)
    if not root:
        return "Invalid base frame"

    allowed_classes = [mode, "Universal"]

    pool = {}
    for node in root.nodes:
        if node.classification in allowed_classes:
            pool.setdefault(node.type_name, []).append(node)

    selected_items = []

    # Mandatory categories
    mandatory = ['body', 'head', 'hair', 'torso', 'legs']
    for cat in mandatory:
        if cat in pool:
            item = rng.choice(pool[cat])
            item.variant = rng.choice(item.variant_list) if item.variant_list else ''
            selected_items.append(item)

    # Optional items
    remaining_cats = [c for c in pool.keys() if c not in mandatory]

    num_optional = rng.randint(2, 5)
    extra_cats = rng.sample(remaining_cats, min(len(remaining_cats), num_optional))

    for cat in extra_cats:
        item = rng.choice(pool[cat])
        item.variant = rng.choice(item.variant_list) if item.variant_list else ''
        selected_items.append(item)

    return selected_items


def create_url(base_frame, items):
    url_param = [item.url_param_format() for item in items]
    url_params = "&".join(url_param)
    return SPRITE_GEN_URL + '/#?' + url_params + '&sex=' + base_frame


class_df = pd.read_csv('classified_items.csv')
class_map = {(row['type_name'], row['name']): row['classification'] for _, row in class_df.iterrows()}
metadata_dict = load_metadata_to_dict()

base_frames = ['child', 'female', 'male', 'muscular', 'pregnant', 'teen']
quick_dict = {frame: Node("base_frame", frame) for frame in base_frames}

# Re-link logic with classification
for type_name, items in metadata_dict.items():
    for item in items:
        name = item.get('name')
        variants = item.get('variants', [])
        reqs = item.get('required', [])

        classification = class_map.get((type_name, name), "Universal")

        item_node = Node(type_name, name, classification, variants)
        for req in reqs:
            if req in quick_dict:
                quick_dict[req].nodes.append(item_node)

base_frame = "male"
mode = "Non-Humanoid"
seed = 100

items = generate_sprite(base_frame, mode, seed)
url = create_url(base_frame, items)
print(url)
