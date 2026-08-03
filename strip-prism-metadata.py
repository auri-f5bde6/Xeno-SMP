import os
import tomlkit
from tomlkit.items import AbstractTable


def delete(metadata):
    for key in list(metadata.keys()):
        if key.startswith("x-prismlauncher-"):
            metadata.pop(key)
        elif isinstance(metadata[key], AbstractTable):
            delete(metadata[key])

for mod in os.listdir("mods"):
    if mod.endswith(".pw.toml"):
        text = None
        with open(os.path.join("mods", mod), "r") as f:
            text = f.read()
        metadata = tomlkit.parse(text)
        delete(metadata)
        with(open(os.path.join("mods", mod), "w")) as f:
            f.write(tomlkit.dumps(metadata))
