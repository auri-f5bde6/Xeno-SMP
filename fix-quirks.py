import os
import tomlkit
from tomlkit.items import AbstractTable


def fix(filename, metadata):
    for key in list(metadata.keys()):
        if key.startswith("x-prismlauncher-"):
            metadata.pop(key)
        elif isinstance(metadata[key], AbstractTable):
            fix(filename, metadata[key])
        elif key=="side" and metadata[key] not in ["client", "server", "both"]:
            print(f"WARNING: {filename} have a invalid side of '{metadata[key]}', falling back to both")
            metadata[key] = "both" # default to both
        elif key=="url" and isinstance(metadata[key], str) and metadata[key].strip()=="":
            print(f"WARNING: {filename} have empty url, deleting field")
            metadata.pop(key)

for mod in os.listdir("mods"):
    if mod.endswith(".pw.toml"):
        text = None
        with open(os.path.join("mods", mod), "r") as f:
            text = f.read()
        metadata = tomlkit.parse(text)
        fix(mod, metadata)
        with(open(os.path.join("mods", mod), "w")) as f:
            f.write(tomlkit.dumps(metadata))
