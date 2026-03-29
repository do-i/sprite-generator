import json
from pathlib import Path
from spriter.item_selector import Generator
from spriter.playwright_wrapper import SpriteDownloader

PARENT_DIR = Path(__file__).parent

def load_config(config_path):
    with open(config_path, 'r') as f:
        config = json.load(f)

    # Convert relative strings to absolute Path objects
    config["metadata_path"] = PARENT_DIR / config["metadata_path"]
    config["classification_path"] = PARENT_DIR / config["classification_path"]
    return config

def main():
    config = load_config(PARENT_DIR / "config.json")
    generator = Generator(config)

    with SpriteDownloader(config["sprite_gen_url"]) as downloader:
        base_frame = config["base_frame"]
        mode = config["mode"]
        mode_mod = mode.replace(" ","-")

        for seed in range(config["range_start"], config["range_end"]):
            sprite_url = generator.generate_sprite_url(base_frame, mode, seed)
            output_file_prefix = f"{base_frame}_{mode_mod}_{seed}.png"
            downloader.download_sprite(sprite_url, output_file_prefix)

if __name__ == "__main__":
    main()