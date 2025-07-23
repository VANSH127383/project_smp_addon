import os
import json
import uuid
import random

# === CONFIGURATION ===
ADDON_NAME = "Project_SMP"
OUTPUT_FOLDER = "final"
VERSION = [1, 0, 0]
RACES = ["angel", "demon", "human"]

# === Helper Functions ===
def create_folder(path):
    os.makedirs(path, exist_ok=True)

def write_file(path, content):
    create_folder(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def generate_manifest(name, description, is_bp=True):
    return {
        "format_version": 2,
        "header": {
            "name": name + (" BP" if is_bp else " RP"),
            "description": description,
            "uuid": str(uuid.uuid4()),
            "version": VERSION,
            "min_engine_version": [1, 21, 0]
        },
        "modules": [
            {
                "type": "data" if is_bp else "resources",
                "uuid": str(uuid.uuid4()),
                "version": VERSION
            }
        ]
    }

# === Create Folder Structure ===
bp_path = os.path.join(OUTPUT_FOLDER, "behavior_pack")
rp_path = os.path.join(OUTPUT_FOLDER, "resource_pack")

create_folder(bp_path)
create_folder(rp_path)

# === Write Manifests ===
write_file(os.path.join(bp_path, "manifest.json"),
           json.dumps(generate_manifest(ADDON_NAME, "Race System Behavior Pack", True), indent=4))

write_file(os.path.join(rp_path, "manifest.json"),
           json.dumps(generate_manifest(ADDON_NAME, "Race System Resource Pack", False), indent=4))

# === Scoreboard Setup ===
setup_scoreboard = """
scoreboard objectives add has_joined dummy
scoreboard objectives add race dummy
"""

for race in RACES:
    setup_scoreboard += f"scoreboard players set @a[scores={{race={RACES.index(race)}}}] race {RACES.index(race)}\n"

write_file(os.path.join(bp_path, "functions/setup_scoreboard.mcfunction"), setup_scoreboard.strip())

# === Tick Logic ===
tick_logic = """
execute as @a[scores={has_joined=0}] at @s run function race_logic/assign_race
"""

write_file(os.path.join(bp_path, "functions/tick.mcfunction"), tick_logic.strip())

# === Random Race Assignment ===
assign_race = """
scoreboard players set @s has_joined 1
"""

for i, race in enumerate(RACES):
    assign_race += f"""
execute if score @s race matches {i} run say You are a {race.capitalize()}!
"""

random_assignment = f"""
scoreboard players set @s race {random.randint(0, len(RACES) - 1)}
"""

write_file(os.path.join(bp_path, "functions/race_logic/assign_race.mcfunction"), (random_assignment + assign_race).strip())
