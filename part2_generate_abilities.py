import os

# === CONFIGURATION ===
OUTPUT_FOLDER = "final"
BEHAVIOR_FUNCTIONS = os.path.join(OUTPUT_FOLDER, "behavior_pack", "functions")
RACES = ["angel", "demon", "human"]

# === Helper Functions ===
def create_folder(path):
    os.makedirs(path, exist_ok=True)

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)

# === Create Folder Structure ===
race_logic_path = os.path.join(BEHAVIOR_FUNCTIONS, "race_logic")
create_folder(race_logic_path)

# === Generate ability_trigger.mcfunction ===
trigger_lines = []

# Scoreboards for action detection (assumed to be created elsewhere)
# Triggers based on slot selection (0-4)
for slot in range(5):
    trigger_lines.append(f"execute as @a[scores={{selected_slot={slot}}}] run function race_logic/use_slot_{slot}")

write_file(os.path.join(race_logic_path, "ability_trigger.mcfunction"), "\n".join(trigger_lines))

# === Generate use_slot_<n>.mcfunction for each slot ===
for slot in range(5):
    lines = [f"# Slot {slot} ability triggers"]
    for race in RACES:
        lines.append(f"execute as @a[scores={{race={RACES.index(race)}}}] run function abilities/{race}/ability{slot if slot != 0 else 'passive'}")
    write_file(os.path.join(race_logic_path, f"use_slot_{slot}.mcfunction"), "\n".join(lines))

# === Generate routing function per race ===
for race in RACES:
    lines = [
        f"# {race.capitalize()} race logic router",
        f"function abilities/{race}/passive",
        f"execute as @a[scores={{selected_slot=1}}] run function abilities/{race}/ability1",
        f"execute as @a[scores={{selected_slot=2}}] run function abilities/{race}/ability2",
        f"execute as @a[scores={{selected_slot=3}}] run function abilities/{race}/ability3",
        f"execute as @a[scores={{selected_slot=4}}] run function abilities/{race}/ability4",
    ]
    write_file(os.path.join(race_logic_path, f"{race}.mcfunction"), "\n".join(lines))

# === Modify tick.mcfunction ===
tick_path = os.path.join(BEHAVIOR_FUNCTIONS, "tick.mcfunction")
if not os.path.exists(tick_path):
    create_folder(os.path.dirname(tick_path))
    with open(tick_path, "w") as f:
        f.write("")

with open(tick_path, "r") as f:
    tick_lines = f.read().splitlines()

inject_line = "function race_logic/ability_trigger"
if inject_line not in tick_lines:
    tick_lines.append(inject_line)

write_file(tick_path, "\n".join(tick_lines))

# === Add needed scoreboards to setup ===
setup_path = os.path.join(BEHAVIOR_FUNCTIONS, "setup_scoreboard.mcfunction")
create_folder(os.path.dirname(setup_path))

setup_lines = []
if os.path.exists(setup_path):
    with open(setup_path, "r") as f:
        setup_lines = f.read().splitlines()

needed = [
    "scoreboard objectives add ability_cd dummy",
    "scoreboard objectives add trial_unlocked dummy",
    "scoreboard objectives add ability3_variant dummy",
]

for line in needed:
    if line not in setup_lines:
        setup_lines.append(line)

write_file(setup_path, "\n".join(setup_lines))
