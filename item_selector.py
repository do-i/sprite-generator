import json
import random
import pandas as pd


class Node:
    def __init__(self, type_name, name, classification="Universal", variants=None):
        self.type_name = type_name
        self.name = name
        self.classification = classification
        self.variant_list = variants or []
        self.variant = ""
        self.nodes = []

    def url_param_format(self):
        resolved_name = self.name.replace(" ", "_")
        return f"{self.type_name}={resolved_name}_{self.variant}"


class Generator:
    def __init__(self, config: dict):
        self.metadata_path = config.get(
            "metadata_path",
            "item-metadata.json"
        )
        self.classification_path = config.get(
            "classification_path",
            "classified_items.csv"
        )
        self.sprite_gen_url = config.get(
            "sprite_gen_url",
            "http://localhost:8000"
        )
        self.base_frames = config.get(
            "base_frames",
            ["child", "female", "male", "muscular", "pregnant", "teen"]
        )
        self.class_map = self._load_class_map()
        self.metadata_dict = self._load_metadata()
        self.graph = self._build_graph()

    # -------------------------
    # private helpers
    # -------------------------
    def _load_class_map(self):
        df = pd.read_csv(self.classification_path)
        return {
            (row["type_name"], row["name"]): row["classification"]
            for _, row in df.iterrows()
        }

    def _load_metadata(self):
        with open(self.metadata_path, "r") as f:
            items = json.load(f)
        type_to_objects = {}
        for item in items.values():
            t_name = item.get("type_name")
            name = item.get("name")
            variants = item.get("variants", [])
            required = item.get("required", [])
            if t_name and name:
                type_to_objects.setdefault(t_name, []).append({
                    "name": name,
                    "variants": variants,
                    "required": required,
                })
        return type_to_objects

    def _build_graph(self):
        quick_dict = {
            frame: Node("base_frame", frame)
            for frame in self.base_frames
        }
        for type_name, items in self.metadata_dict.items():
            for item in items:
                name = item["name"]
                variants = item.get("variants", [])
                reqs = item.get("required", [])
                classification = self.class_map.get(
                    (type_name, name),
                    "Universal",
                )
                node = Node(
                    type_name=type_name,
                    name=name,
                    classification=classification,
                    variants=variants,
                )
                for req in reqs:
                    if req in quick_dict:
                        quick_dict[req].nodes.append(node)
        return quick_dict

    def _generate_items(self, root, mode, rng):
        allowed_classes = [mode, "Universal"]
        pool = {}
        for node in root.nodes:
            if node.classification in allowed_classes:
                pool.setdefault(node.type_name, []).append(node)
        selected_items = []
        mandatory = [
            "body",
            "head",
            "hair",
            "torso",
            "legs",
        ]
        for cat in mandatory:
            if cat in pool:
                item = rng.choice(pool[cat])
                item.variant = (
                    rng.choice(item.variant_list)
                    if item.variant_list
                    else ""
                )
                selected_items.append(item)
        remaining_cats = [
            c for c in pool.keys()
            if c not in mandatory
        ]
        num_optional = rng.randint(2, 5)
        extra_cats = rng.sample(
            remaining_cats,
            min(len(remaining_cats), num_optional),
        )
        for cat in extra_cats:
            item = rng.choice(pool[cat])
            item.variant = (
                rng.choice(item.variant_list)
                if item.variant_list
                else ""
            )
            selected_items.append(item)
        return selected_items

    def _create_url(self, root, items):
        params = "&".join(
            item.url_param_format()
            for item in items
        )
        return f"{self.sprite_gen_url}/#{params}&sex={root.name}"


    # -------------------------
    # public API
    # -------------------------
    def generate_sprite_url(
        self,
        base_frame: str,
        mode: str = "Humanoid",
        seed: int | None = None,
    ) -> str:
        rng = random.Random(seed)
        root = self.graph.get(base_frame)
        if not root:
            raise ValueError(f"Invalid base_frame: {base_frame}")
        items = self._generate_items(root, mode, rng)
        return self._create_url(root, items)