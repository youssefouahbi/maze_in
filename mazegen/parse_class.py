import os
from typing import Tuple, Optional


class ConfigParser:
    def __init__(self, path: str) -> None:
        self.width: int
        self.height: int
        self.entry: Tuple[int, int]
        self.exit: Tuple[int, int]
        self.perfect: bool
        self.seed: Optional[int]
        self.algo: str
        self.output_file: str

        self._parse(path)

    # ==========================
    # PARSING
    # ==========================

    def _parse(self, file_path: str) -> None:

        # ---------- FILE VALIDATION ----------

        if not os.path.exists(file_path):
            raise FileNotFoundError("ERROR: config file not found")

        if not file_path.endswith(".txt"):
            raise ValueError("ERROR: config file must be a .txt file")

        if os.path.getsize(file_path) == 0:
            raise ValueError("ERROR: config file is empty")

        required_keys = {
            "WIDTH", "HEIGHT", "ENTRY", "EXIT",
            "PERFECT", "SEED", "ALGO", "OUTPUT_FILE"
        }

        config: dict[str, str] = {}

        with open(file_path, "r") as f:
            lines = f.readlines()

        # ---------- LINE BY LINE ----------

        for line_num, raw_line in enumerate(lines, start=1):
            line = raw_line.strip()

            if not line or line.startswith("#"):
                continue

            if line.count("=") != 1:
                raise SyntaxError(f"Line {line_num}: invalid '=' usage")

            key, raw_value = line.split("=")

            if " " in key:
                raise SyntaxError(f"Line {line_num}: whitespace in key name")

            if key == "":
                raise SyntaxError(f"Line {line_num}: empty key")

            if raw_value == "":
                raise SyntaxError(f"Line {line_num}: empty value")

            if key not in required_keys:
                raise KeyError(f"Line {line_num}: unknown key '{key}'")

            if key in config:
                raise KeyError(f"Line {line_num}: duplicate key '{key}'")

            config[key] = raw_value

        # ---------- MISSING KEYS ----------

        missing = required_keys - config.keys()
        if missing:
            raise KeyError(f"ERROR: missing keys → {', '.join(missing)}")

        # ==========================
        # TYPE VALIDATION
        # ==========================

        # WIDTH
        if "." in config["WIDTH"]:
            raise ValueError("WIDTH must be integer")

        try:
            self.width = int(config["WIDTH"])
        except ValueError:
            raise ValueError("WIDTH must be integer")

        if self.width < 10 or self.width > 100:
            raise ValueError("WIDTH out of range (10–100)")

        # HEIGHT
        if "." in config["HEIGHT"]:
            raise ValueError("HEIGHT must be integer")

        try:
            self.height = int(config["HEIGHT"])
        except ValueError:
            raise ValueError("HEIGHT must be integer")

        if self.height < 10 or self.height > 100:
            raise ValueError("HEIGHT out of range (10–100)")

        # SEED
        seed_value = config["SEED"]
        if seed_value.lower() == "none":
            self.seed = None
        else:
            try:
                self.seed = int(seed_value)
            except ValueError:
                raise ValueError("SEED must be an integer or None")
            if self.seed < 0:
                raise ValueError("SEED cannot be negative")
        # ENTRY
        entry_parts = config["ENTRY"].split(",")
        if len(entry_parts) != 2:
            raise SyntaxError("ENTRY must be row,col")

        self.entry = (int(entry_parts[0]), int(entry_parts[1]))

        # EXIT
        exit_parts = config["EXIT"].split(",")
        if len(exit_parts) != 2:
            raise SyntaxError("EXIT must be row,col")

        self.exit = (int(exit_parts[0]), int(exit_parts[1]))

        # PERFECT
        if config["PERFECT"] not in {"True", "False"}:
            raise ValueError("PERFECT must be True or False")

        self.perfect = config["PERFECT"] == "True"

        # ALGO
        self.algo = config["ALGO"].upper()
        if self.algo not in {"DFS", "PRIM"}:
            raise ValueError("ALGO must be DFS or PRIM")

        # OUTPUT_FILE
        self.output_file = config["OUTPUT_FILE"]

        if not self.output_file.endswith(".txt"):
            raise ValueError("OUTPUT_FILE must be .txt")

        if " " in self.output_file:
            raise ValueError("OUTPUT_FILE must not contain spaces")

        # ==========================
        # GLOBAL VALIDATION
        # ==========================

        if self.entry[0] >= self.width or self.entry[1] >= self.height:
            raise ValueError("ENTRY out of bounds")

        if self.exit[0] >= self.width or self.exit[1] >= self.height:
            raise ValueError("EXIT out of bounds")

        if self.entry == self.exit:
            raise ValueError("ENTRY and EXIT cannot be identical")
