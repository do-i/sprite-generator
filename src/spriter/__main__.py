from spriter.item_selector import Generator
from spriter.playwright_wrapper import SpriteDownloader
from pathlib import Path

PARENT_DIR = Path(__file__).parent
SPRITE_GEN_URL = "http://mima:8000"

def main():
    config = {
        "metadata_path": PARENT_DIR / "item-metadata.json",
        "classification_path": PARENT_DIR / "classified_items.csv",
        "sprite_gen_url": SPRITE_GEN_URL
    }

    generator = Generator(config)

    with SpriteDownloader(SPRITE_GEN_URL) as downloader:
        for seed in range(1,50):
            sprite_url = generator.generate_sprite_url(
                base_frame="male",
                mode="Non-Humanoid",
                seed=seed,
            )

            downloader.download_sprite(
                sprite_url,
                filename=f"sprite_{seed}.png"
            )

if __name__ == "__main__":
    main()
