import os
from typing import Union, Dict, Tuple

ConfigValue = Union[int, bool, str, Tuple[int, int]]


def read_config(file_path: str) -> Dict[str, ConfigValue]:
    required_keys = {
        'WIDTH', 'HEIGHT', 'ENTRY', 'EXIT',
        'PERFECT', 'SEED', 'ALGO', 'OUTPUT_FILE'
    }

    config: Dict[str, ConfigValue] = {}

    # ==========================
    # FILE VALIDATION
    # ==========================

    if not os.path.exists(file_path):
        raise FileNotFoundError("ERROR: config file not found")

    if not file_path.endswith(".txt"):
        raise ValueError("ERROR: config file must be a .txt file")

    if os.path.getsize(file_path) == 0:
        raise ValueError("ERROR: config file is empty")

    # ==========================
    # PARSING
    # ==========================

    with open(file_path, "r") as f:
        lines = f.readlines()

    for line_num, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()

        # Ignore comments & empty lines
        if not line or line.startswith("#"):
            continue

        # Must contain exactly one "="
        if line.count("=") != 1:
            raise SyntaxError(f"Line {line_num}: invalid '=' usage")

        key, raw_value = line.split("=")
        value: ConfigValue = raw_value

        # Whitespace in key
        if " " in key:
            raise SyntaxError(f"Line {line_num}: whitespace in key name")

        # Empty key or value
        if key == "":
            raise SyntaxError(f"Line {line_num}: empty key")

        if raw_value == "":
            raise SyntaxError(f"Line {line_num}: empty value")

        # Unknown key
        if key not in required_keys:
            raise KeyError(f"Line {line_num}: unknown key '{key}'")

        # Duplicate key
        if key in config:
            raise KeyError(f"Line {line_num}: duplicate key '{key}'")

        # ==========================
        # TYPE VALIDATION
        # ==========================

        if key in {"WIDTH", "HEIGHT", "SEED"}:

            # Reject float
            if "." in raw_value:
                raise ValueError(f"Line {line_num}: {key} must be an integer")

            try:
                int_value = int(raw_value)
            except ValueError:
                raise ValueError(f"Line {line_num}: {key} must be an integer")

            if int_value < 0:
                raise ValueError(f"Line {line_num}: {key} cannot be negative")

            if key in {"WIDTH", "HEIGHT"}:
                if int_value < 10:
                    raise ValueError(
                        f"Line {line_num}: {key} below minimum (10)"
                    )
                if int_value > 100:
                    raise ValueError(
                        f"Line {line_num}: {key} above maximum (100)")
            value = int_value

        elif key in {"ENTRY", "EXIT"}:

            parts = raw_value.split(",")

            if len(parts) != 2:
                raise SyntaxError(
                    f"Line {line_num}: {key} must be in format row,col"
                )

            try:
                row = int(parts[0])
                col = int(parts[1])
            except ValueError:
                raise ValueError(
                    f"Line {line_num}: {key} coordinates must be integers"
                )

            if row < 0 or col < 0:
                raise ValueError(
                    f"Line {line_num}: {key} cannot have negative coordinates"
                )

            value = (row, col)

        elif key == "PERFECT":

            if raw_value not in {"True", "False"}:
                raise ValueError(
                    f"Line {line_num}: PERFECT must be True or False"
                )

            value = raw_value == "True"

        elif key == "ALGO":

            algo = raw_value.upper()
            if algo not in {"DFS", "PRIM"}:
                raise ValueError(
                    f"Line {line_num}: ALGO must be DFS or PRIM"
                )
            value = algo

        elif key == "OUTPUT_FILE":

            if not raw_value.endswith(".txt"):
                raise ValueError(
                    f"Line {line_num}: OUTPUT_FILE must be a .txt file"
                )
            if raw_value.count(" ") >= 1:
                raise ValueError(
                    f"Line {line_num}: OUTPUT_FILE contain spaces !"
                )
            value = raw_value

        config[key] = value

    # ==========================
    # GLOBAL VALIDATION
    # ==========================

    missing = required_keys - config.keys()
    if missing:
        raise KeyError(f"ERROR: missing keys → {', '.join(missing)}")

    width = config["WIDTH"]
    height = config["HEIGHT"]
    entry = config["ENTRY"]
    exit_ = config["EXIT"]

    assert isinstance(width, int)
    assert isinstance(height, int)
    assert isinstance(entry, tuple)
    assert isinstance(exit_, tuple)

    en1, en2 = entry
    ex1, ex2 = exit_

    if en1 >= width or en2 >= height:
        raise ValueError("out of bound")
    elif ex1 >= width or ex2 >= height:
        raise ValueError("out of bound")

    # Bounds check (order independent)
    if entry == exit_:
        raise ValueError("ERROR: ENTRY and EXIT cannot be identical")

    return config
