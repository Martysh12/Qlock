import json


def load_config():
    with open("conf.json", "r") as f:
        return json.load(f)


def save_config(config):
    with open("conf.json", "w") as f:
        return json.dump(config, f)
