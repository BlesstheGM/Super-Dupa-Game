import os

# Use relative path for the data file
DATA_FILE = os.path.join("data", "characters.txt")

def initialize_data_file():
    """Ensure the data file exists and is initialized."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            pass

def get_character_data(name):
    """
    Fetch the character's data (level, coins, deaths).
    If the character doesn't exist, return default values.
    """
    initialize_data_file()
    with open(DATA_FILE, "r") as file:
        for line in file:
            char_name, level, coins, deaths = line.strip().split(":")
            if char_name == name:
                return int(level), int(coins), int(deaths)
    return 1, 0, 0  # Default level 1, 0 coins, 0 deaths

def update_character_level(name, new_level):
    """
    Update the character's level in the data file.
    """
    initialize_data_file()
    lines = []
    found = False
    with open(DATA_FILE, "r") as file:
        for line in file:
            char_name, level, coins, deaths = line.strip().split(":")
            if char_name == name:
                lines.append(f"{char_name}:{new_level}:{coins}:{deaths}\n")
                found = True
            else:
                lines.append(line)
    if not found:
        # Add new entry for the character
        lines.append(f"{name}:{new_level}:0:0\n")
    with open(DATA_FILE, "w") as file:
        file.writelines(lines)

def update_character_coins(name, new_coins):
    """
    Update the character's coins in the data file.
    """
    initialize_data_file()
    lines = []
    found = False
    with open(DATA_FILE, "r") as file:
        for line in file:
            char_name, level, coins, deaths = line.strip().split(":")
            if char_name == name:
                lines.append(f"{char_name}:{level}:{new_coins}:{deaths}\n")
                found = True
            else:
                lines.append(line)
    if not found:
        # Add new entry for the character
        lines.append(f"{name}:1:{new_coins}:0\n")
    with open(DATA_FILE, "w") as file:
        file.writelines(lines)

def update_character_deaths(name, new_deaths):
    """
    Update the character's deaths in the data file.
    """
    initialize_data_file()
    lines = []
    found = False
    with open(DATA_FILE, "r") as file:
        for line in file:
            char_name, level, coins, deaths = line.strip().split(":")
            if char_name == name:
                lines.append(f"{char_name}:{level}:{coins}:{new_deaths}\n")
                found = True
            else:
                lines.append(line)
    if not found:
        # Add new entry for the character
        lines.append(f"{name}:1:0:{new_deaths}\n")
    with open(DATA_FILE, "w") as file:
        file.writelines(lines)
