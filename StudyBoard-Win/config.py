import yaml

with open("./config.yaml", "r", encoding="utf-8") as fp:
    _obj = yaml.safe_load(fp)

api = _obj["api"]
token = _obj["token"]
