#!/bin/python3
import os
import subprocess
import yaml

value_file = "ngrok-value.yaml"
with open(f"../deploy/{value_file}", 'r') as filename:
    try:
        values = yaml.load(filename, Loader=yaml.FullLoader)
        chart = values["metadata"]["chart"]
        name = values["metadata"]["name"]
        repoUrl = values["metadata"]["repoUrl"] if "repoUrl" in values["metadata"] else None
        namespace = values["metadata"]["namespace"]
        directInstallation = values["metadata"]["directInstallation"] if "directInstallation" in values["metadata"] else False
        otherOptions = values["metadata"]["otherOptions"] if "otherOptions" in values["metadata"] else ''
        preInstallation = values["metadata"]["preInstallation"] if "preInstallation" in values["metadata"] else None
        chart_name = chart.split("/")[-1]
    except yaml.YAMLError as exc:
        print(exc)
if preInstallation:
    subprocess.run(preInstallation,shell=True,encoding="utf-8")

if repoUrl is not None:
    helm_repo_cmd = f'helm repo add {name} {repoUrl}'
    subprocess.run(helm_repo_cmd, shell=True, capture_output=True, text=True)

if directInstallation:
    helm_cmd = f'helm upgrade --install {name} {chart} --namespace {namespace} --create-namespace {otherOptions}'
else:
    helm_cmd = f'helm upgrade --install -f ../deploy/{value_file} {name} {chart} --namespace {namespace} --create-namespace {otherOptions}'
print(helm_cmd)
result = subprocess.run(helm_cmd, shell=True, capture_output=True, text=True, encoding="utf-8")
if result.returncode != 0:
    print(f"Error running helm command: {result.stderr}")