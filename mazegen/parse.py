import os


def read_config(file_path):
    required_keys = {
        'WIDTH', 'HEIGHT', 'ENTRY', 'EXIT',
        'PERFECT', 'SEED', 'ALGO', 'OUTPUT_FILE'
    }

    config = {}

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

        key, value = line.split("=")

        # Whitespace in key
        if " " in key:
            raise SyntaxError(f"Line {line_num}: whitespace in key name")

        # Empty key or value
        if key == "":
            raise SyntaxError(f"Line {line_num}: empty key")

        if value == "":
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
            if "." in value:
                raise ValueError(f"Line {line_num}: {key} must be an integer")

            try:
                value = int(value)
            except ValueError:
                raise ValueError(f"Line {line_num}: {key} must be an integer")

            if value < 0:
                raise ValueError(f"Line {line_num}: {key} cannot be negative")

            if key in {"WIDTH", "HEIGHT"}:
                if value < 10:
                    raise ValueError(
                        f"Line {line_num}: {key} below minimum (10)"
                    )
                if value > 100:
                    raise ValueError(
                        f"Line {line_num}: {key} above maximum (100)"
                    )

        elif key in {"ENTRY", "EXIT"}:

            parts = value.split(",")

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

            if value not in {"True", "False"}:
                raise ValueError(
                    f"Line {line_num}: PERFECT must be True or False"
                )

            value = value == "True"

        elif key == "ALGO":

            value = value.upper()
            if value not in {"DFS", "PRIM"}:
                raise ValueError(
                    f"Line {line_num}: ALGO must be DFS or PRIM"
                )

        elif key == "OUTPUT_FILE":

            if not value.endswith(".txt"):
                raise ValueError(
                    f"Line {line_num}: OUTPUT_FILE must be a .txt file"
                )
            if value.count(" ") >= 1:
                raise ValueError(
                    f"Line {line_num}: OUTPUT_FILE contain spaces !"
                )

        config[key] = value

    # ==========================
    # GLOBAL VALIDATION
    # ==========================

    missing = required_keys - config.keys()
    if missing:
        raise KeyError(f"ERROR: missing keys → {', '.join(missing)}")

    width = config["WIDTH"]
    height = config["HEIGHT"]

    en1, en2 = config["ENTRY"]
    ex1, ex2 = config["EXIT"]

    if en1 >= width or en2 >= height:
        raise ValueError("out of bound")
    elif ex1 >= width or ex2 >= height:
        raise ValueError("out of bound")
        

    # if en1 * en2 >= band or ex1 * ex2 >= band:
    #     raise ValueError("out of bound")

    # Bounds check (order independent)
    if config["ENTRY"] == config["EXIT"]:
        raise ValueError("ERROR: ENTRY and EXIT cannot be identical")

    return config


# ==========================
# TEST
# ==========================
if __name__ == "__main__":
    try:
        cfg = read_config("config.txt")
        print("Configuration valid")
        print(cfg)
    except Exception as e:
        print(e)