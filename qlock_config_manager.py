import json

def generate_default_config():
    with open("conf.json", "w") as f:
        return json.dump(
            {
                "text_color": [255, 255, 255],
                "background_color": [0, 0, 0],
                "opacity": 0.67,
                "font_face": "Noto Sans",
                "font_size": 14,
                "size": [539, 364],
                "radius": [50, 50]
            },
            f
        )

def load_config():
    try:
        with open("conf.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        generate_default_config()

        return load_config()

def save_config(config):
    with open("conf.json", "w") as f:
        return json.dump(config, f)
