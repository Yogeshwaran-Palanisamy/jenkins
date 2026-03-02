#!/bin/python3
import os
import subprocess
import yaml

value_file = os.listdir("deploy")
print(value_file)
for file in value_file:
    if file.endswith(".yaml"):
        with open(f"deploy/{file}", 'r') as filename:
            try:
                values = yaml.load(filename, Loader=yaml.FullLoader)
                chart = values["metadata"]["chart"]
                name = values["metadata"]["name"]
                repoUrl = values["metadata"]["repoUrl"] if "repoUrl" in values["metadata"] else None
                namespace = values["metadata"]["namespace"]
                chart_name = chart.split("/")[-1]
            except yaml.YAMLError as exc:
                print(exc)
    if repoUrl is not None:
        helm_repo_cmd = f'helm repo add {name} {repoUrl}'
        subprocess.run(helm_repo_cmd, shell=True, capture_output=True, text=True)
    helm_cmd = f'helm upgrade --install -f deploy/{file} {name} {chart} --namespace {namespace} --create-namespace'
    result = subprocess.run(helm_cmd, shell=True, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        print(f"Error running helm command: {result.stderr}")