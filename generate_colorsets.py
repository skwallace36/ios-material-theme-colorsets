import json
import os
import sys

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return {
        "red": f"0x{hex_color[0:2]}",
        "green": f"0x{hex_color[2:4]}",
        "blue": f"0x{hex_color[4:6]}",
        "alpha": "1.000"
    }

def parse_material_theme(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    schemes = data.get("schemes", {})
    light_colors = schemes.get("light", {})
    dark_colors = schemes.get("dark", {})

    matched_colors = {key: {"light": light_colors.get(key), "dark": dark_colors.get(key)}
                      for key in light_colors.keys() & dark_colors.keys()}

    return matched_colors

def create_colorset_folders(matched_colors, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for color_name, colors in matched_colors.items():
        folder_path = os.path.join(output_dir, f"{color_name}.colorset")
        os.makedirs(folder_path, exist_ok=True)

        colorset_data = {
            "colors": [
                {
                    "color": {
                        "color-space": "srgb",
                        "components": hex_to_rgb(colors["light"])
                    },
                    "idiom": "universal"
                },
                {
                    "appearances": [
                        {
                            "appearance": "luminosity",
                            "value": "dark"
                        }
                    ],
                    "color": {
                        "color-space": "srgb",
                        "components": hex_to_rgb(colors["dark"])
                    },
                    "idiom": "universal"
                }
            ],
            "info": {
                "author": "xcode",
                "version": 1
            }
        }

        json_path = os.path.join(folder_path, "Contents.json")
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(colorset_data, json_file, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <path_to_json> <output_directory>")
        sys.exit(1)

    json_file_path = sys.argv[1]
    output_directory = sys.argv[2]

    theme_data = parse_material_theme(json_file_path)
    create_colorset_folders(theme_data, output_directory)
