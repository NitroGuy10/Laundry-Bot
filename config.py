import json
import os

CONFIG_PATH = "config.json"
config = {
    "discord_bot_token": "",
    "port": "52800",
    "silenced": "false",
    "finished_timeout_seconds": "60"
}

def save_config() -> None:
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

# Returns True if the discord_bot_token is set
def load_config() -> bool:
    if os.path.exists(CONFIG_PATH):
        # Load existing config
        found_token = False
        with open(CONFIG_PATH, "r") as f:
            loaded_config = json.load(f)
            for key in config:
                if key in loaded_config and loaded_config[key] != "":
                    config[key] = loaded_config[key]
                    if key == "discord_bot_token":
                        found_token = True
        
        # Save the config back to file to ensure all keys are present
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=4)
            
        if not found_token:
            print("Please fill in discord_bot_token in config.json.")
        return found_token

    else:
        print("Config file not found. Please fill in discord_bot_token in newly-generated config.json.")
        # Create new config file containing only discord_bot_token
        with open(CONFIG_PATH, "w") as f:
            json.dump({ "discord_bot_token": "" }, f, indent=4)
        return False

def get(key: str) -> str:
    return config[key]

def set(key: str, value: str) -> None:
    config[key] = value
    save_config()




