import yaml

def load(path="config.yaml"):
    with open(path, 'r') as fp:
        result = yaml.load(fp.read())

    return result
