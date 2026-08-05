import os
from typing import Callable
from urllib.parse import urlsplit
import tomlkit
from tomlkit.container import Container
from tomlkit.items import AbstractTable


def for_each_mod(func: Callable[[str, Container, str], None],
                 warning: Callable[[str], str | None] = lambda filename: None) -> None:
    def new_func(filename, metadata: Container):
        for key in list(metadata.keys()):
            if isinstance(metadata[key], AbstractTable):
                new_func(filename, metadata[key])
            else:
                func(filename, metadata, key)

    for mod in os.listdir("mods"):
        if mod.endswith(".pw.toml"):
            text = None
            with open(os.path.join("mods", mod), "r") as f:
                text = f.read()
            metadata = tomlkit.parse(text)
            new_func(mod, metadata)
            with(open(os.path.join("mods", mod), "w")) as f:
                f.write(tomlkit.dumps(metadata))
        else:
            warn_text = warning(mod)
            if warn_text is not None:
                print(warn_text)


def fix(filename, metadata, key):
    if key.startswith("x-prismlauncher-"):
        metadata.pop(key)
    elif key == "side" and metadata[key] not in ["client", "both"]: # server sided mod doesnt get added to mrpack ...
        print(f"WARNING: {filename} have a invalid side of '{metadata[key]}', falling back to both")
        metadata[key] = "both"  # default to both
    elif key == "url" and isinstance(metadata[key], str) and metadata[key].strip() == "":
        print(f"WARNING: {filename} have empty url, deleting field")
        metadata.pop(key)


def check(filename, metadata, key):
    if key == "url":
        url = urlsplit(metadata[key])
        if url.netloc != "cdn.modrinth.com":
            print(f"WARNING: {filename} has non modrinth cdn url of: {url.netloc}, full url: {metadata[key]}")


for_each_mod(fix)
for_each_mod(check, lambda filename: f"WARNING: Binary data in mod folder: {filename}")
