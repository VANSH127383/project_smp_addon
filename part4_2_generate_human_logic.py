import os

# === CONFIGURATION ===
OUTPUT_FOLDER = "final"
BP_FUNCTIONS = os.path.join(OUTPUT_FOLDER, "behavior_pack", "functions")
TICK_FUNCTION_PATH = os.path.join(BP_FUNCTIONS, "tick.mcfunction")

HUMAN_SWORD_NAME = "Dragon Slayer"
SWORD_SLOT = 0

HUMAN_FOLDER = os.path.join(BP_FUNCTIONS, "abilities", "human")
PLAYER_STATE_FOLDER = os.path.join(BP_FUNCTIONS, "player_state")
RACE_LOGIC_FOLDER = os.path.join(BP_FUNCTIONS, "race_logic")

# === HELPERS ===
def create_folder(path):
    os.makedirs(path, exist_ok=True)

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

def append_to_file_if_missing(path, lines):
    if not os.path.exists(path):
        write_file(path, "\n".join(lines))
        return
    with open(path, "r", encoding="utf-8") as f:
        existing = f.read()
    with open(path, "a", encoding="utf-8") as f:
        for line in lines:
            if line not in existing:
                f.write(line + "\n")

def delete_file(path):
    if os.path.exists(path):
        os.remove(path)

# === 1. CREATE FOLDERS ===
for folder in [HUMAN_FOLDER, PLAYER_STATE_FOLDER, RACE_LOGIC_FOLDER]:
    create_folder(folder)

# === 2. DELETE OLD HUMAN ABILITIES (except passive) ===
for i in range(1, 5):
    delete_file(os.path.join(HUMAN_FOLDER, f"ability{i}.mcfunction"))
delete_file(os.path.join(HUMAN_FOLDER, "ability3A.mcfunction"))
delete_file(os.path.join(HUMAN_FOLDER, "ability3B.mcfunction"))

# === 3. HUMAN SWORD CHECK ===
sword_check_code = f"""
# Give sword if race is human
execute as @a[scores={{race=2}}] unless entity @s[hasitem={{location=slot.hotbar.{SWORD_SLOT}, item=stick, name=\\"{HUMAN_SWORD_NAME}\\"}}] run give @s stick{{display:{{Name:'"{HUMAN_SWORD_NAME}"'}},tag:["human_sword"]}} 1

# Remove sword if not human
execute as @a[scores={{race=!2}}] if entity @s[hasitem={{item=stick, name=\\"{HUMAN_SWORD_NAME}\\"}}] run clear @s stick 0 1
"""
write_file(os.path.join(RACE_LOGIC_FOLDER, "human_sword_check.mcfunction"), sword_check_code)

# === 4. PLAYER STATE DETECTION ===
write_file(os.path.join(PLAYER_STATE_FOLDER, "detect_jump.mcfunction"),
           'execute as @a[on_ground=false] run scoreboard players set @s is_jumping 1')
write_file(os.path.join(PLAYER_STATE_FOLDER, "detect_sneak.mcfunction"),
           'execute as @a[nbt={Sneaking:1b}] run scoreboard players set @s is_sneaking 1')
write_file(os.path.join(PLAYER_STATE_FOLDER, "detect_attack.mcfunction"),
           'execute as @a[scores={has_attacked=1..}] run scoreboard players set @s is_attacking 1')

# === 5. ABILITY TRIGGER ENTRY ===
ability_trigger_code = f"""
# Human-specific sword logic
execute as @a[scores={{race=2,selected_slot={SWORD_SLOT}}}] if entity @s[hasitem={{location=slot.hotbar.{SWORD_SLOT}, item=stick, name=\\"{HUMAN_SWORD_NAME}\\"}}] run function race_logic/trigger_human_combo
"""
write_file(os.path.join(RACE_LOGIC_FOLDER, "ability_trigger.mcfunction"), ability_trigger_code)

# === 6. COMBO LOGIC ===
combo_logic = """
# Human Sword Ability Combos (with variant 3A / 3B)
scoreboard players reset @s ability_trigger

# Sneak + right click → Ability 3A or 3B depending on variant
execute as @a[scores={is_sneaking=1,ability3_variant=0}] run function abilities/human/sword_ability3A
execute as @a[scores={is_sneaking=1,ability3_variant=1}] run function abilities/human/sword_ability3B

# Jump + right click → Ability 2
execute as @a[scores={is_jumping=1}] run function abilities/human/sword_ability2

# Right click (no sneak/jump) → Ability 1
execute as @a[scores={is_jumping=0,is_sneaking=0}] run function abilities/human/sword_ability1

# Jump + attack → Ability 4
execute as @a[scores={is_jumping=1,is_attacking=1}] run function abilities/human/sword_ability4
"""
write_file(os.path.join(RACE_LOGIC_FOLDER, "trigger_human_combo.mcfunction"), combo_logic)

# === 7. CREATE SWORD ABILITY PLACEHOLDERS ===
for ability in ["sword_ability1", "sword_ability2", "sword_ability3A", "sword_ability3B", "sword_ability4"]:
    ability_path = os.path.join(HUMAN_FOLDER, f"{ability}.mcfunction")
    if not os.path.exists(ability_path):
        write_file(ability_path, f"# {ability} placeholder\nsay {ability} triggered")

# === 8. PRESERVE OR CREATE PASSIVE ===
passive_path = os.path.join(HUMAN_FOLDER, "passive.mcfunction")
if not os.path.exists(passive_path):
    write_file(passive_path, "# Human passive ability\nsay Human passive is active")

# === 9. APPEND PLAYER STATE & CHECK TO TICK ===
tick_calls = [
    "function player_state/detect_jump",
    "function player_state/detect_sneak",
    "function player_state/detect_attack",
    "function race_logic/human_sword_check"
]
append_to_file_if_missing(TICK_FUNCTION_PATH, tick_calls)

print("✅ Part 4.2 updated with:")
print("✔️ Old human ability files removed")
print("✔️ Sword abilities created with variant 3A/3B")
print("✔️ Tick file updated")
