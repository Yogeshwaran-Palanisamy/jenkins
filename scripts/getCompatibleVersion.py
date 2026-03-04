import yaml
import os
import requests
import json

params = {
    "version": "2.541.2"
}
os.chdir(f"./deploy")
with open("jenkins-value.yaml","r",encoding="utf-8") as f:
    loaded_file = yaml.safe_load(f)
    plugins = loaded_file["controller"]["installPlugins"]

with open("new_plugins.yaml","w") as f:
    new_plugins = (requests.get("https://updates.jenkins.io/update-center.actual.json",params=params)).json()
    for plugin in plugins:
        new_plugins_list = ":".join((new_plugins["plugins"][plugin.split(":")[0]]["gav"]).split(":")[1:])
        f.writelines("  - " + new_plugins_list + "\n")