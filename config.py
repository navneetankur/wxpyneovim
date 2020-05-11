import json
class Config:
    def __init__(self):
        with open('keymap.json') as fp:
            self.keymap = json.load(fp,object_pairs_hook=key_to_int)
        with open('keycodemap.json') as fp:
            self.keycodemap = json.load(fp,object_pairs_hook=key_to_int)
        with open('settings.json') as fp:
            self.settings = json.load(fp)
def key_to_int(x):
    return {int(k): v for k, v in x}
