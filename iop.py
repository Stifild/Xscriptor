import json

class InputOutputProcessor:
    def __init__(self):
        pass

    def load_json(self, json_file: str) -> dict:
        with open(json_file, 'r') as f:
            return json.load(f)
    
    def save_json(self, json_file: str, data: dict):
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)
    