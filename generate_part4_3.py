import os

# === CONFIGURATION ===
OUTPUT_FOLDER = "final"
ABILITIES = {
    "ability1": 30,
    "ability2": 45,
    "ability3": 60,
    "ability4": 105
}
HUMAN_LOGIC_PATH = os.path.join(OUTPUT_FOLDER, "behavior_pack", "functions", "race_logic", "human.mcfunction")
SETUP_PATH = os.path.join(OUTPUT_FOLDER, "behavior_pack", "functions", "setup_scoreboard.mcfunction")

# === Helper Functions ===
def create_folder(path):
    os.makedirs(path, exist_ok=True)

def append_scoreboard_setup(scoreboard_lines):
    if not os.path.exists(SETUP_PATH):
        create_folder(os.path.dirname(SETUP_PATH))
        with open(SETUP_PATH, "w", encoding="utf-8") as f:
            f.write("\n".join(scoreboard_lines) + "\n")
    else:
        with open(SETUP_PATH, "r+", encoding="utf-8") as f:
            content = f.read()
            f.seek(0, 2)
            for line in scoreboard_lines:
                if line not in content:
                    f.write(line + "\n")

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# === Step 1: Append required scoreboards for advanced triggering ===
scoreboards_needed = [
    "scoreboard objectives add is_jumping dummy",
    "scoreboard objectives add is_sneaking dummy",
    "scoreboard objectives add using_item dummy",
    "scoreboard objectives add selected_slot dummy",
    "scoreboard objectives add last_slot dummy"
]
append_scoreboard_setup(scoreboards_needed)

# === Step 2: Generate human.mcfunction logic ===
lines = [
    "# === HUMAN ABILITY TRIGGERS ===",
    "# Ability 1 - Right click (no jump/sneak)",
    "execute as @a[scores={race=2,using_item=1,is_jumping=0,is_sneaking=0}] if score @s selected_slot matches 0..8 run function abilities/human/ability1",

    "# Ability 2 - Jump + Right click",
    "execute as @a[scores={race=2,using_item=1,is_jumping=1}] if score @s selected_slot matches 0..8 run function abilities/human/ability2",

    "# Ability 3 - Sneak + Right click",
    "execute as @a[scores={race=2,using_item=1,is_sneaking=1}] if score @s selected_slot matches 0..8 run function abilities/human/ability3",

    "# Ability 4 - Jump + Left click (mob hit)",
    "execute as @a[scores={race=2,is_jumping=1}] at @s run function abilities/human/ability4"
]

create_folder(os.path.dirname(HUMAN_LOGIC_PATH))
write_file(HUMAN_LOGIC_PATH, "\n".join(lines))

print("✅ Part 4.3: Human sword advanced trigger logic generated successfully.")
