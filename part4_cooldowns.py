import os

# === CONFIG ===
OUTPUT_FOLDER = "final"
RACES = ["angel", "demon", "human"]
ABILITIES = ["ability1", "ability2", "ability3a", "ability3b", "ability4"]
COOLDOWNS = {
    "ability1": 30,
    "ability2": 45,
    "ability3a": 60,
    "ability3b": 60,
    "ability4": 105
}

# === HELPERS ===
def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# === 1. Add scoreboard objectives ===
def patch_scoreboard_setup():
    path = os.path.join(OUTPUT_FOLDER, "behavior_pack/functions/setup_scoreboard.mcfunction")
    if not os.path.exists(path):
        print(f"Missing: {path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    new_lines = list(lines)
    for race in RACES:
        for ab in ABILITIES:
            obj = f"{race}_{ab}_cd"
            cmd = f"scoreboard objectives add {obj} dummy"
            if not any(obj in line for line in lines):
                new_lines.append(cmd)

    write_file(path, "\n".join(new_lines))

# === 2. Cooldown tick logic ===
def patch_tick_function():
    tick_path = os.path.join(OUTPUT_FOLDER, "behavior_pack/functions/tick.mcfunction")
    logic_path = os.path.join(OUTPUT_FOLDER, "behavior_pack/functions/race_logic/cooldown_tick.mcfunction")

    tick_call = "function race_logic/cooldown_tick"

    if os.path.exists(tick_path):
        with open(tick_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        if tick_call not in lines:
            lines.append(tick_call)
        write_file(tick_path, "\n".join(lines))
    else:
        write_file(tick_path, tick_call)

    logic_lines = []
    for race in RACES:
        for ab in ABILITIES:
            logic_lines.append(
                f"execute as @a[tag=race:{race}] if score @s {race}_{ab}_cd matches 1.. run scoreboard players remove @s {race}_{ab}_cd 1"
            )

    write_file(logic_path, "\n".join(logic_lines))

# === 3. Patch each ability file ===
def patch_ability_triggers():
    for race in RACES:
        for ab in ABILITIES:
            file_path = os.path.join(OUTPUT_FOLDER, f"behavior_pack/functions/abilities/{race}/{ab}.mcfunction")
            if not os.path.exists(file_path):
                print(f"⛔ Skipping missing: {file_path}")
                continue

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Prevent double-patching
            if f"{race}_{ab}_cd" in content and "scoreboard players set" in content:
                print(f"⚠️ Already patched: {file_path}")
                continue

            patched = []
            patched.append(f"# COOLDOWN CHECK")
            patched.append(f"execute if score @s {race}_{ab}_cd matches 1.. run function misc/ability_on_cooldown")

            if ab == "ability4":
                patched.append("execute unless score @s trial_unlocked matches 1.. run function misc/trial_locked")

            patched.append("# --- Original Ability Logic ---")
            patched.append(content.strip())
            patched.append(f"# Apply cooldown")
            patched.append(f"scoreboard players set @s {race}_{ab}_cd {COOLDOWNS[ab]}")

            write_file(file_path, "\n".join(patched))
            print(f"✅ Patched: {file_path}")

# === MAIN RUN ===
if __name__ == "__main__":
    patch_scoreboard_setup()
    patch_tick_function()
    patch_ability_triggers()
    print("✅ Part 4 complete!")
