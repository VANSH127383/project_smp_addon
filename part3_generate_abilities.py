import os

# === CONFIG ===
OUTPUT_FOLDER = "final"
ABILITIES = {
    "angel": {
        "passive": "Heaven's Barrier - Infinite protection from mobs/projectiles (Gojo Infinity)",
        "ability1": "Divine Ascent - Elytra + rocket boost every 2s for 10s",
        "ability2": "Sanctified Recovery - Regeneration III for 10s",
        "ability3a": "Chrono Lock - Freeze enemies in place for 3–5s",
        "ability3b": "Chrono Reversal - Teleport back + restore HP",
        "ability4": "Judgment Ray - AoE beam that damages, levitates, glows enemies"
    },
    "demon": {
        "passive": "Cursed Flesh - Strength II always active",
        "ability1": "Demonic Leap - Jump with AoE knockback/damage",
        "ability2": "Malevolent Regen - AoE lifesteal from mobs",
        "ability3a": "Domain Eruption - Slam explosion (Gojo-style)",
        "ability3b": "Reverse Curse - Full heal + shockwave push",
        "ability4": "Cursed Calamity - Domain slashes all enemies except user"
    },
    "human": {
        "passive": "None (Human uses a sword with advanced ability triggers)",
        "ability1": "Dash Strike - Right click in air (sword required)",
        "ability2": "Blade Flurry - Jump + right click",
        "ability3a": "Shadow Bind - Sneak + right click",
        "ability3b": "Sniper Slash - Sneak + right click (variant)",
        "ability4": "Final Resolve - Jump + hit mob → heal, buff for 30s"
    }
}

FUNCTIONS_PATH = os.path.join(OUTPUT_FOLDER, "behavior_pack", "functions")
ABILITIES_FOLDER = os.path.join(FUNCTIONS_PATH, "abilities")

def create_folder(path):
    os.makedirs(path, exist_ok=True)

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())

# === Generate ability files ===
for race in ABILITIES:
    race_folder = os.path.join(ABILITIES_FOLDER, race)
    create_folder(race_folder)

    for ability_key, ability_desc in ABILITIES[race].items():
        file_path = os.path.join(race_folder, f"{ability_key}.mcfunction")
        content = f"""
# {race.capitalize()} - {ability_key}
# {ability_desc}
say Using {ability_key} for {race}
# TODO: Add particles, damage logic, and effects here
"""
        write_file(file_path, content)

print("✅ Part 3 abilities generated successfully.")
