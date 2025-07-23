import os

# === CONFIGURATION ===
OUTPUT_FOLDER = os.path.join("final", "behavior_pack")
SWORD_NAME = "dragon_slayer"
CUSTOM_ITEM_NAME = f"{SWORD_NAME}:item.{SWORD_NAME}"
SLOT = 0  # Hotbar slot index (0 = first)

# === HELPER FUNCTIONS ===
def create_folder(path):
    os.makedirs(path, exist_ok=True)

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# === Create folders ===
create_folder(os.path.join(OUTPUT_FOLDER, "functions", "give_items"))
create_folder(os.path.join(OUTPUT_FOLDER, "functions", "race_logic"))

# === give_dragon_slayer.mcfunction ===
give_sword = f"""give @s {CUSTOM_ITEM_NAME}
replaceitem entity @s slot.hotbar {SLOT} {CUSTOM_ITEM_NAME}
"""

write_file(
    os.path.join(OUTPUT_FOLDER, "functions", "give_items", "give_dragon_slayer.mcfunction"),
    give_sword
)

# === check_sword_owner.mcfunction ===
check_script = f"""# Remove sword if not Human (race 2)
execute as @a unless score @s race matches 2 run clear @s {CUSTOM_ITEM_NAME}

# Give sword if Human and doesn't already have it
execute as @a[scores={{race=2}}] unless entity @s[hasitem={{item={CUSTOM_ITEM_NAME}, location=slot.hotbar}}] run function give_items/give_dragon_slayer

# Force sword to stay in slot {SLOT}
execute as @a[hasitem={{item={CUSTOM_ITEM_NAME}, location=slot.hotbar}}] run replaceitem entity @s slot.hotbar {SLOT} {CUSTOM_ITEM_NAME}
"""

write_file(
    os.path.join(OUTPUT_FOLDER, "functions", "race_logic", "check_sword_owner.mcfunction"),
    check_script
)

# === Inject check_sword_owner into tick.mcfunction ===
tick_path = os.path.join(OUTPUT_FOLDER, "functions", "tick.mcfunction")
inject_line = "function race_logic/check_sword_owner"

if os.path.exists(tick_path):
    with open(tick_path, "r+", encoding="utf-8") as f:
        lines = f.read().splitlines()
        if inject_line not in lines:
            lines.append(inject_line)
            f.seek(0)
            f.write("\n".join(lines) + "\n")
            f.truncate()
else:
    write_file(tick_path, inject_line + "\n")

print("✅ Fixed: Human-exclusive Dragon Slayer sword system generated successfully.")
