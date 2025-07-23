import os

# === CONFIGURATION ===
OUTPUT_FOLDER = "final"
ABILITIES = {
    "ability1": 30,
    "ability2": 45,
    "ability3": 60,
    "ability4": 105
}
TRIGGER_PATH = os.path.join(OUTPUT_FOLDER, "behavior_pack", "functions", "race_logic")
HUMAN_ABILITY_PATH = os.path.join(OUTPUT_FOLDER, "behavior_pack", "functions", "abilities", "human")

# === Helper Functions ===
def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content.strip() + "\n")

# === Generate 4.4 Human Ability Trigger System ===
human_ability_trigger_code = f"""
# Part 4.4 - Human Ability Trigger System

# Ability 1: Right click in air (triggered via 'right_click_air' == 1)
execute as @a[scores={{race=2, right_click_air=1, human_ability1_cd=0}}] run function abilities/human/ability1

# Ability 2: Jump + Right Click (jumping==1 + right_click_air==1)
execute as @a[scores={{race=2, is_jumping=1, right_click_air=1, human_ability2_cd=0}}] run function abilities/human/ability2

# Ability 3: Sneak + Right Click (sneaking==1 + right_click_air==1)
execute as @a[scores={{race=2, is_sneaking=1, right_click_air=1, human_ability3_cd=0}}] if score @s ability3_variant matches 0 run function abilities/human/ability3a
execute as @a[scores={{race=2, is_sneaking=1, right_click_air=1, human_ability3_cd=0}}] if score @s ability3_variant matches 1 run function abilities/human/ability3b

# Ability 4: Jump + Left Click on mob (right_click_air==0 + left_click==1 + is_jumping==1 + target_score==1)
execute as @a[scores={{race=2, is_jumping=1, left_click_entity=1, human_ability4_cd=0}}] run function abilities/human/ability4

# Reset all flags for next tick
scoreboard players set @a right_click_air 0
scoreboard players set @a left_click_entity 0
scoreboard players set @a is_sneaking 0
scoreboard players set @a is_jumping 0
"""

write_file(os.path.join(TRIGGER_PATH, "human_trigger.mcfunction"), human_ability_trigger_code)

"Part 4.4 completed: 'human_trigger.mcfunction' generated and ready."
