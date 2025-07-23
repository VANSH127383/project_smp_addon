import os
import json
from PIL import Image

# === CONFIG ===
ROOT_FOLDER = "final"
RESOURCE_FOLDER = os.path.join(ROOT_FOLDER, "resource_pack")
ITEM_NAME = "dragon_slayer"
TEXTURE_NAME = f"item.{ITEM_NAME}"
TEXTURE_PATH = f"textures/items/{ITEM_NAME}.png"

# === Helper Functions ===
def create_folder(path):
    os.makedirs(path, exist_ok=True)

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# === Folder Setup ===
texture_folder = os.path.join(RESOURCE_FOLDER, "textures", "items")
create_folder(texture_folder)

# === Add Placeholder Texture ===
img = Image.new("RGBA", (16, 16), (255, 0, 0, 255))  # Red placeholder
img.save(os.path.join(RESOURCE_FOLDER, TEXTURE_PATH))

# === Modify item_texture.json ===
texture_json_path = os.path.join(RESOURCE_FOLDER, "textures", "item_texture.json")
item_texture = load_json(texture_json_path)

# Ensure correct structure
if "texture_data" not in item_texture:
    item_texture["texture_data"] = {}

item_texture["texture_data"][TEXTURE_NAME] = {
    "textures": TEXTURE_PATH
}

save_json(texture_json_path, item_texture)

print(f"✅ Resource added: {TEXTURE_PATH}")
print(f"✅ item_texture.json updated with '{TEXTURE_NAME}'")
