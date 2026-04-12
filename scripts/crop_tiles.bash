#!/usr/bin/env bash

mkdir -p ./generated_spritesheets/subsets

for file in ./generated_spritesheets/male_Non-Humanoid_*.png; do
    [[ -f "$file" ]] || continue

    dest="./generated_spritesheets/subsets/$(basename "$file")"

    if [[ -f "$dest" ]]; then
        echo "Skipping: $file"
        continue
    fi

    echo "Cropping: $file"
    magick "$file" -crop 576x768+0+0 "$dest"
done

echo "Finished."