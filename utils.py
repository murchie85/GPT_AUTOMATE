import yaml
import sys

def validate_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            yaml.safe_load(file)
        print(f"The YAML file '{file_path}' is valid.")
        return(True)
    except yaml.YAMLError as e:
        print(f"The YAML file '{file_path}' is not valid.")
        print(e)
        return(False)