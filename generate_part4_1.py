import os

# === CONFIG ===
RACES = ["angel", "demon", "human"]
ABILITIES = {
    "ability1": 30,
    "ability2": 45,
    "ability3": 60,
    "ability4": 105
}
OUTPUT_FOLDER = "final"
BEHAVIOR_PATH = os.path.join(OUTPUT_FOLDER, "behavior_pack")
COOLDOWN_PATH = os.path.join(BEHAVIOR_PATH, "functions", "cooldowns")
TICK_FILE = os.path.join(BEHAVIOR_PATH, "functions", "tick.mcfunction")
SETUP_FILE = os.path.join(BEHAVIOR_PATH, "functions", "setup_scoreboard.mcfunction")

# === UTILS ===
def create_folder(path):
    os.makedirs(path, exist_ok=True)

def write_file(path, content):
    with open(path, 'w', encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# === GENERATE COOLDOWN FUNCTION FILES ===
def generate_cooldown_functions():
    for race in RACES:
        lines = [f"# Cooldowns for {race} abilities"]
        for ability, seconds in ABILITIES.items():
            lines.append(f"# {ability} cooldown")
            lines.append(f"execute as @a[scores={{ {race}_{ability}_cd=1.. }}] run scoreboard players remove @s {race}_{ability}_cd 1")
            lines.append("")
        file_path = os.path.join(COOLDOWN_PATH, f"{race}.mcfunction")
        write_file(file_path, "\n".join(lines))

# === APPEND TO TICK FUNCTION ===
def inject_into_tick():
    tick_lines = []
    for race in RACES:
        tick_lines.append(f"function cooldowns/{race}")

    if os.path.exists(TICK_FILE):
        with open(TICK_FILE, "r", encoding="utf-8") as f:
            existing = f.read()
        if "# >> cooldown system" not in existing:
            with open(TICK_FILE, "a", encoding="utf-8") as f:
                f.write("\n# >> cooldown system\n" + "\n".join(tick_lines) + "\n")
    else:
        write_file(TICK_FILE, "# >> cooldown system\n" + "\n".join(tick_lines))

# === ADD TO SETUP SCOREBOARDS ===
def setup_scoreboards():
    if not os.path.exists(SETUP_FILE):
        write_file(SETUP_FILE, "")
    
    with open(SETUP_FILE, "r", encoding="utf-8") as f:
        existing = f.read()
    
    if "# >> cooldown scoreboards" not in existing:
        with open(SETUP_FILE, "a", encoding="utf-8") as f:
            f.write("\n# >> cooldown scoreboards\n")
            for race in RACES:
                for ability in ABILITIES:
                    f.write(f"scoreboard objectives add {race}_{ability}_cd dummy\n")

# === MAIN ===
def main():
    create_folder(COOLDOWN_PATH)
    generate_cooldown_functions()
    inject_into_tick()
    setup_scoreboards()
    print("✅ Part 4.1 cooldown system successfully integrated.")

if __name__ == "__main__":
    main()
