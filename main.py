from item_selector import Generator

if __name__ == "__main__":
    config = {
        "metadata_path": "item-metadata.json",
        "classification_path": "classified_items.csv",
        "sprite_gen_url": "http://mima:8000"
    }
    generator = Generator(config)
    sprite_url = generator.generate_sprite_url(
        base_frame = "male",
        mode = "Non-Humanoid",
        seed = 1,
    )
    print(f"sprite: {sprite_url}")
