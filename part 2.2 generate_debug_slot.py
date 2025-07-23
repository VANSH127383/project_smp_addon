import os

# === CONFIG ===
OUTPUT_FOLDER = "final"
DEBUG_FILE_PATH = os.path.join(OUTPUT_FOLDER, "behavior_pack", "functions", "debug_selected_slot.mcfunction")

def create_folder(path):
    os.makedirs(path, exist_ok=True)

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())

# === Generate tellraw-based debug output ===
debug_lines = [
    'tellraw @s {"rawtext":[{"text":"§eSelected Slot: §a"}, {"score":{"name":"@s","objective":"selected_slot"}}]}',
    'tellraw @s {"rawtext":[{"text":"§7Last Slot: §c"}, {"score":{"name":"@s","objective":"last_slot"}}]}'
]

# === Create folders and write debug file ===
create_folder(os.path.dirname(DEBUG_FILE_PATH))
write_file(DEBUG_FILE_PATH, "\n".join(debug_lines))

print("✅ Debug slot function generated: debug_selected_slot.mcfunction")
