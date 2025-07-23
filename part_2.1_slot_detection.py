import os

# === CONFIGURATION ===
OUTPUT_FOLDER = "final"
BEHAVIOR_PATH = os.path.join(OUTPUT_FOLDER, "behavior_pack")
FUNCTIONS_PATH = os.path.join(BEHAVIOR_PATH, "functions")

TICK_FN = os.path.join(FUNCTIONS_PATH, "tick.mcfunction")
SCOREBOARD_FN = os.path.join(FUNCTIONS_PATH, "setup_scoreboard.mcfunction")

# === Ensure parent folders exist ===
os.makedirs(FUNCTIONS_PATH, exist_ok=True)

def add_to_file(path, extra_code, check_line=None):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(extra_code.strip() + "\n")
        return

    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    if check_line and any(check_line.strip() in line for line in lines):
        return  # Already injected

    with open(path, "a", encoding="utf-8") as f:
        f.write("\n" + extra_code.strip() + "\n")

# === Scoreboards Setup ===
scoreboards_code = """
# Track selected slot for auto ability triggering
scoreboard objectives add selected_slot dummy
scoreboard objectives add last_slot dummy
"""
add_to_file(SCOREBOARD_FN, scoreboards_code, check_line="selected_slot")

# === Inject logic into tick.mcfunction ===
tick_code = """
# Track hotbar slot selection change
execute as @a store result score @s selected_slot run data get entity @s SelectedItemSlot

# Detect and trigger ability on slot change
execute as @a if score @s selected_slot != @s last_slot run function race_logic/ability_trigger

# Update slot memory
execute as @a run scoreboard players operation @s last_slot = @s selected_slot
"""
add_to_file(TICK_FN, tick_code, check_line="selected_slot")

print("✅ [Part 2.1] Slot detection logic injected correctly without duplication.")
