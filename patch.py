import os

# === CONFIGURATION ===
OUTPUT_FOLDER = "final/behavior_pack"
FUNCTIONS_PATH = os.path.join(OUTPUT_FOLDER, "functions")
TICK_PATH = os.path.join(FUNCTIONS_PATH, "tick.mcfunction")
SETUP_PATH = os.path.join(FUNCTIONS_PATH, "setup_scoreboard.mcfunction")
TICK_TAG_PATH = os.path.join(OUTPUT_FOLDER, "tags", "tick.json")

# === Files to inject in tick.mcfunction ===
REQUIRED_TICK_FUNCTIONS = [
    "function race_logic/ability_trigger",
    "function race_logic/check_sword_owner",
    "function trials/trial_unlock",
    "function cooldowns/angel",
    "function cooldowns/demon",
    "function cooldowns/human",
    "function race_logic/human_trigger",
    "function debug_selected_slot",
    "execute as @a[scores={race=0}] run function abilities/angel/passive",
    "execute as @a[scores={race=1}] run function abilities/demon/passive",
    "execute as @a[scores={race=2}] run function abilities/human/passive",
]

# === Scoreboards to ensure in setup_scoreboard.mcfunction ===
REQUIRED_SCOREBOARDS = [
    "scoreboard objectives add race dummy",
    "scoreboard objectives add has_joined dummy",
    "scoreboard objectives add selected_slot dummy",
    "scoreboard objectives add last_slot dummy",
    "scoreboard objectives add is_jumping dummy",
    "scoreboard objectives add is_sneaking dummy",
    "scoreboard objectives add using_item dummy",
    "scoreboard objectives add right_click_air dummy",
    "scoreboard objectives add left_click_entity dummy",
    "scoreboard objectives add trial_unlocked dummy",
    "scoreboard objectives add ability3_variant dummy",
]

# === Ensure directory exists ===
def create_folder(path):
    os.makedirs(path, exist_ok=True)

# === Ensure lines exist in a file ===
def append_lines_if_missing(path, lines):
    create_folder(os.path.dirname(path))
    if os.path.exists(path):
        with open(path, "r+", encoding="utf-8") as f:
            content = f.read().splitlines()
            for line in lines:
                if line not in content:
                    content.append(line)
            f.seek(0)
            f.write("\n".join(content) + "\n")
            f.truncate()
    else:
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

# === Fix tick.json ===
def fix_tick_json():
    tick_data = {"values": ["tick"]}
    tick_folder = os.path.dirname(TICK_TAG_PATH)
    create_folder(tick_folder)
    with open(TICK_TAG_PATH, "w", encoding="utf-8") as f:
        import json
        json.dump(tick_data, f, indent=4)

# === MAIN PATCHER ===
def patch_all():
    append_lines_if_missing(TICK_PATH, REQUIRED_TICK_FUNCTIONS)
    append_lines_if_missing(SETUP_PATH, REQUIRED_SCOREBOARDS)
    fix_tick_json()
    return "✅ All core logic fixed: tick functions, passives, scoreboard setup, and tick.json patched."

patch_all()
