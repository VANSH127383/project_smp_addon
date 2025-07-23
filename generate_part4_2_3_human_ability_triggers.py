import os

# === CONFIG ===
ADDON_NAME = "Project_SMP"
OUTPUT_FOLDER = "final"
BP_PATH = os.path.join(OUTPUT_FOLDER, "behavior_pack")  # ✅ FIXED

# === PATHS ===
HUMAN_FUNCTION_PATH = os.path.join(BP_PATH, "functions", "abilities", "human")
ROUTING_FUNCTION_PATH = os.path.join(BP_PATH, "functions", "race_logic", "human_sword_trigger.mcfunction")
MAIN_FN_PATH = os.path.join(BP_PATH, "functions", "race_logic", "human_sword_main.mcfunction")
SLOT0_FN_PATH = os.path.join(BP_PATH, "functions", "race_logic", "human_slot0.mcfunction")

# === Create required folders (safely) ===
os.makedirs(HUMAN_FUNCTION_PATH, exist_ok=True)
os.makedirs(os.path.dirname(ROUTING_FUNCTION_PATH), exist_ok=True)

# === Write human_sword_trigger.mcfunction ===
with open(ROUTING_FUNCTION_PATH, "w") as f:
    f.write("\n".join([
        "# Human sword ability routing",
        "execute if score @s race matches 2 if score @s human_sword_check matches 1 run function race_logic/human_sword_main"
    ]))

# === Write human_sword_main.mcfunction ===
with open(MAIN_FN_PATH, "w") as f:
    f.write("\n".join([
        "# Human sword main ability logic",
        "execute if score @s selected_slot matches 0 run function race_logic/human_slot0"
    ]))

# === Write human_slot0.mcfunction ===
slot_logic = [
    "# Ability 1 — Right Click (Not sneaking)",
    "execute if score @s is_sneaking matches 0 if score @s ability1_cd matches 0 run function abilities/human/ability1",
    "",
    "# Ability 2 — Jump + Right Click",
    "execute if score @s is_jumping matches 1 if score @s ability2_cd matches 0 run function abilities/human/ability2",
    "",
    "# Ability 3 — Sneak + Right Click (variant-based)",
    "execute if score @s is_sneaking matches 1 if score @s ability3_cd matches 0 if score @s ability3_variant matches 0 run function abilities/human/ability3a",
    "execute if score @s is_sneaking matches 1 if score @s ability3_cd matches 0 if score @s ability3_variant matches 1 run function abilities/human/ability3b",
    "",
    "# Ability 4 — Jump + Left Click on mob (AoE)",
    "execute if score @s is_jumping matches 1 if score @s ability4_cd matches 0 run function abilities/human/ability4"
]
with open(SLOT0_FN_PATH, "w") as f:
    f.write("\n".join(slot_logic))

print("✅ Part 4.2.3 generated successfully without creating duplicate folders.")
