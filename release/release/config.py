import os, configparser
cfg = configparser.ConfigParser()
cfg.read(["docker.cfg", os.path.expanduser("~/.docker.cfg")], encoding="utf-8")

name = cfg.get("user","name")
mail = cfg.get("user","mail")
comment =cfg.get("user","comment", fallback="")

del cfg

repoBase = "/work/source"
debianBase = "/work/debian"
obsBase = "/work/osc/Kontact:4.13:Development"

epoch={"kdepim-runtime": "4:",
        "kdepim": "4:",
        "kdepimlibs": "4:",
        "kfilemetadata": "4:",
        "baloo": "4:",
        }
