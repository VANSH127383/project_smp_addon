import os

# === CONFIG ===
OUTPUT_FOLDER = "final/behavior_pack"
FUNCTIONS_PATH = os.path.join(OUTPUT_FOLDER, "functions")
TRIALS_PATH = os.path.join(FUNCTIONS_PATH, "trials")
TICK_PATH = os.path.join(FUNCTIONS_PATH, "tick.mcfunction")
SETUP_PATH = os.path.join(FUNCTIONS_PATH, "setup_scoreboard.mcfunction")

RACES = {
    "angel": 0,
    "demon": 1,
    "human": 2
}

# === HELPERS ===
def create_folder(path):
    os.makedirs(path, exist_ok=True)

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

def append_to_file_if_missing(path, line):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(line + "\n")
        return
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if line not in content:
        with open(path, "a", encoding="utf-8") as f:
            f.write(line + "\n")

# === 1. Setup scoreboard objectives ===
def setup_scoreboards():
    create_folder(FUNCTIONS_PATH)
    content = ""
    if os.path.exists(SETUP_PATH):
        with open(SETUP_PATH, "r", encoding="utf-8") as f:
            content = f.read()
    with open(SETUP_PATH, "a", encoding="utf-8") as f:
        if "trial_unlocked" not in content:
            f.write("scoreboard objectives add trial_unlocked dummy\n")
        if "ability3_variant" not in content:
            f.write("scoreboard objectives add ability3_variant dummy\n")

# === 2. Generate trial unlock routing file ===
def generate_trial_unlock():
    lines = [
        "# Trial unlock routing by race",
    ]
    for race, score in RACES.items():
        lines.append(f"execute as @a[scores={{race={{{score}}}}}] unless score @s trial_unlocked matches 1 run function trials/{race}_trial")
    write_file(os.path.join(TRIALS_PATH, "trial_unlock.mcfunction"), "\n".join(lines))

# === 3. Generate individual trial files ===
def generate_trial_files():
    # Angel trial placeholder: player has diamond in inventory
    angel = [
        "# Angel trial unlock condition",
        'execute if entity @s[nbt={Inventory:[{id:"minecraft:diamond",Count:1b}]}] run scoreboard players set @s trial_unlocked 1',
        'execute if score @s trial_unlocked matches 1 run scoreboard players set @s ability3_variant 1'
    ]
    # Demon trial placeholder: player holding netherite sword
    demon = [
        "# Demon trial unlock condition",
        'execute if entity @s[nbt={SelectedItem:{id:"minecraft:netherite_sword"}}] run scoreboard players set @s trial_unlocked 1',
        'execute if score @s trial_unlocked matches 1 run scoreboard players set @s ability3_variant 1'
    ]
    # Human trial placeholder: player killed 5 mobs (scoreboard mob_kills)
    human = [
        "# Human trial unlock condition",
        'execute if score @s mob_kills matches 5.. run scoreboard players set @s trial_unlocked 1',
        'execute if score @s trial_unlocked matches 1 run scoreboard players set @s ability3_variant 1'
    ]

    write_file(os.path.join(TRIALS_PATH, "angel_trial.mcfunction"), "\n".join(angel))
    write_file(os.path.join(TRIALS_PATH, "demon_trial.mcfunction"), "\n".join(demon))
    write_file(os.path.join(TRIALS_PATH, "human_trial.mcfunction"), "\n".join(human))

# === 4. Append trial unlock call to tick.mcfunction ===
def patch_tick():
    line = "function trials/trial_unlock"
    append_to_file_if_missing(TICK_PATH, line)

# === MAIN ===
def main():
    create_folder(TRIALS_PATH)
    setup_scoreboards()
    generate_trial_unlock()
    generate_trial_files()
    patch_tick()
    print("✅ Part 5 trial unlock system generated successfully.")

if __name__ == "__main__":
    main()
