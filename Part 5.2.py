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

# === Real ability effects ===
ABILITY_EFFECTS = {
    "angel": {
        "passive": [
            "effect give @s resistance 1 255 true",
            "particle dust 1 1 1 1 ^ ^1 ^ 0.2 normal"
        ],
        "ability1": [
            "clear @s elytra",
            "replaceitem entity @s slot.weapon.chest 1 elytra",
            "function race_logic/angel/boost_timer"
        ],
        "ability2": [
            "effect give @s regeneration 10 2 true"
        ],
        "ability4": [
            "execute at @s run particle minecraft:dragon_breath ~ ~5 ~ 1 1 1 0 100",
            "execute at @s run effect give @e[r=5,type=!player] levitation 3 1 true",
            "execute at @s run effect give @e[r=5,type=!player] glowing 6 1 true",
            "execute at @s run damage @e[r=5,type=!player] 10 entity_attack"
        ]
    },
    "demon": {
        "passive": [
            "effect give @s strength 1 1 true"
        ],
        "ability1": [
            "tp @s ~ ~5 ~",
            "execute at @s run damage @e[r=4,type=!player] 6 entity_attack",
            "execute at @s run particle minecraft:explosion_emitter ~ ~1 ~"
        ],
        "ability2": [
            "execute at @s run effect give @e[r=6,type=!player] instant_damage 1 1 true",
            "effect give @s instant_health 1 1 true"
        ],
        "ability4": [
            "execute at @s run particle minecraft:dragon_breath ~ ~1 ~ 1 1 1 0 100",
            "function race_logic/demon/slash_loop"
        ]
    },
    "human": {
        "passive": [
            "# No passive ability"
        ],
        "ability1": [
            "tp @s ^ ^ ^3",
            "execute at @s run damage @e[r=3,type=!player] 5 entity_attack",
            "particle minecraft:crit ~ ~1 ~"
        ],
        "ability2": [
            "summon armor_stand ^ ^1 ^ {Tags:[\"blade_throw\"],Invisible:1b,Marker:1b}",
            "function race_logic/human/blade_logic"
        ],
        "ability4": [
            "effect give @s resistance 10 2 true",
            "effect give @s speed 10 2 true",
            "execute at @s run damage @e[r=5,type=!player] 10 entity_attack"
        ]
    }
}

# === Helper functions content ===
HELPER_FUNCTIONS = {
    "race_logic/angel/boost_timer.mcfunction": "\n".join([
        "scoreboard players set @s boost_timer 0",
        "schedule function race_logic/angel/boost_tick 1t"
    ]),
    "race_logic/angel/boost_tick.mcfunction": "\n".join([
        "scoreboard players add @s boost_timer 1",
        "execute if score @s boost_timer matches 1..5 run give @s firework_rocket 1",
        "execute if score @s boost_timer matches 1..5 run function race_logic/angel/boost_tick"
    ]),
    "race_logic/demon/slash_loop.mcfunction": "\n".join([
        "scoreboard players set @s slash_tick 0",
        "schedule function race_logic/demon/slash_tick 1t"
    ]),
    "race_logic/demon/slash_tick.mcfunction": "\n".join([
        "scoreboard players add @s slash_tick 1",
        "execute at @s run damage @e[r=6,type=!player] 3 magic",
        "execute at @s run particle minecraft:soul_fire_flame ~ ~1 ~",
        "execute if score @s slash_tick matches ..5 run schedule function race_logic/demon/slash_tick 4t"
    ]),
    "race_logic/human/blade_logic.mcfunction": "\n".join([
        "execute as @e[tag=blade_throw] at @s run tp @s ^ ^ ^1",
        "execute as @e[tag=blade_throw] at @s run particle minecraft:crit ~ ~ ~",
        "execute as @e[tag=blade_throw] at @s run damage @e[r=1,type=!player] 6 entity_attack",
        "execute as @e[tag=blade_throw] if entity @e[r=1,type=!player] run kill @s"
    ])
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

        # Passive Ability File
        passive_path = os.path.join(race_folder, "passive.mcfunction")
        write_file(passive_path, "\n".join(ABILITY_EFFECTS[race]["passive"]))
        print(f"✅ Generated passive: {race}/passive.mcfunction")

        for ability_key in ABILITIES:
            file_path = os.path.join(race_folder, f"{ability_key}.mcfunction")
            lines = []
            lines.append(f"execute if score @s {race}_{ability_key}_cd matches 1.. run return")

            if ability_key in ["ability3a", "ability3b", "ability4"]:
                lines.append("execute unless score @s trial_unlocked matches 1.. run return")

            if ability_key in ABILITY_EFFECTS[race]:
                lines.extend(ABILITY_EFFECTS[race][ability_key])
            else:
                lines.append(f"say {race.capitalize()} uses {ability_key}!")

            lines.append(f"scoreboard players set @s {race}_{ability_key}_cd {ABILITIES[ability_key]}")
            write_file(file_path, "\n".join(lines))
            print(f"✅ Updated: {race}/{ability_key}.mcfunction")

def generate_helper_functions():
    for relative_path, content in HELPER_FUNCTIONS.items():
        full_path = os.path.join(OUTPUT_FOLDER, relative_path.replace("/", os.sep))
        create_folder(os.path.dirname(full_path))
        write_file(full_path, content)
        print(f"✅ Helper function created: {relative_path}")

if __name__ == "__main__":
    generate_ability_files()
    generate_helper_functions()
    print("✅ Part 5.2 complete — real effects + helper files generated.")
