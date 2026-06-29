#!/usr/bin/env python3
import sys

try:
    import yaml
except ImportError:
    yaml = None


def load_simple_yaml(path):
    if yaml:
        with open(path, "r", encoding="utf-8") as handle:
            return yaml.safe_load(handle)
    data = {}
    stack = [(-1, data)]
    with open(path, "r", encoding="utf-8") as handle:
        for raw in handle:
            line = raw.split("#", 1)[0].rstrip()
            if not line.strip() or ":" not in line:
                continue
            indent = len(line) - len(line.lstrip(" "))
            key, value = line.strip().split(":", 1)
            value = value.strip().strip('"')
            while stack and indent <= stack[-1][0]:
                stack.pop()
            parent = stack[-1][1]
            if value:
                parent[key] = value
            else:
                parent[key] = {}
                stack.append((indent, parent[key]))
    return data


def get_value(data, dotted_key):
    value = data
    for part in dotted_key.split("."):
        value = value[part]
    return value


def main():
    if len(sys.argv) != 3:
        print("Usage: read_project_value.py PROJECT.yaml dotted.key", file=sys.stderr)
        sys.exit(2)
    print(get_value(load_simple_yaml(sys.argv[1]), sys.argv[2]))


if __name__ == "__main__":
    main()
