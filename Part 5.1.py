import os

# === CONFIG ===
OUTPUT_FOLDER = "final/behavior_pack/functions"
RACES = ["angel", "demon", "human"]
ABILITIES = {
    "ability1": 30,
    "ability2": 45,
    "ability3a": 60,
    "ability3b": 60,
    "ability4": 105
}

# Sample ability effects per race and ability (replace with real commands/effects)
ABILITY_EFFECTS = {
    "angel": {
        "ability1": [
            "# Angel Ability 1 - Divine Ascent",
            "say Angel uses Divine Ascent!",
            "# TODO: Add Elytra + rocket boost logic here"
        ],
        "ability2": [
            "# Angel Ability 2 - Sanctified Recovery",
            "effect give @s regeneration 10 2 true"
        ],
        "ability3a": [
            "# Angel Ability 3A - Chrono Lock",
            "say Angel uses Chrono Lock to freeze enemies"
        ],
        "ability3b": [
            "# Angel Ability 3B - Chrono Reversal",
            "say Angel uses Chrono Reversal to heal and teleport"
        ],
        "ability4": [
            "# Angel Ability 4 - Judgment Ray",
            "say Angel uses Judgment Ray to damage enemies"
        ]
    },
    "demon": {
        "ability1": [
            "# Demon Ability 1 - Demonic Leap",
            "say Demon uses Demonic Leap!"
        ],
        "ability2": [
            "# Demon Ability 2 - Malevolent Regen",
            "say Demon uses Malevolent Regen!"
        ],
        "ability3a": [
            "# Demon Ability 3A - Domain Eruption",
            "say Demon slams the ground causing an explosion"
        ],
        "ability3b": [
            "# Demon Ability 3B - Reverse Curse",
            "say Demon uses Reverse Curse to heal and push enemies"
        ],
        "ability4": [
            "# Demon Ability 4 - Cursed Calamity",
            "say Demon creates a cursed domain"
        ]
    },
    "human": {
        "ability1": [
            "# Human Ability 1 - Dash Punch",
            "say Human uses Dash Punch!"
        ],
        "ability2": [
            "# Human Ability 2 - Throwing Blade",
            "say Human throws a blade!"
        ],
        "ability3a": [
            "# Human Ability 3A - Shadow Trap",
            "say Human sets a Shadow Trap!"
        ],
        "ability3b": [
            "# Human Ability 3B - Sniper Shot",
            "say Human fires a Sniper Shot!"
        ],
        "ability4": [
            "# Human Ability 4 - Final Resolve",
            "say Human uses Final Resolve!"
        ]
    }
}

def create_folder(path):
    os.makedirs(path, exist_ok=True)

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

def generate_ability_files():
    for race in RACES:
        race_folder = os.path.join(OUTPUT_FOLDER, "abilities", race)
        create_folder(race_folder)
        for ability_key in ABILITIES:
            file_path = os.path.join(race_folder, f"{ability_key}.mcfunction")
            lines = []
            # Cooldown check
            lines.append(f"execute if score @s {race}_{ability_key}_cd matches 1.. run return")
            
            # Trial unlock check for ability3a, ability3b, and ability4
            if ability_key in ["ability3a", "ability3b", "ability4"]:
                lines.append(f"execute unless score @s trial_unlocked matches 1.. run return")
            
            # Ability effect commands
            lines.extend(ABILITY_EFFECTS[race][ability_key])
            
            # Set cooldown at end
            cooldown_value = ABILITIES[ability_key]
            lines.append(f"scoreboard players set @s {race}_{ability_key}_cd {cooldown_value}")
            
            write_file(file_path, "\n".join(lines))
            print(f"✅ Generated ability file: {race}/{ability_key}.mcfunction")

if __name__ == "__main__":
    generate_ability_files()
    print("✅ Part 5.1 ability files generated with trial unlock and cooldown checks.")
