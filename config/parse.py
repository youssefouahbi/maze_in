def read_config(file_path):
    config = {}
    required_keys = {'WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'PERFECT', 'SEED', 'ALGO'}

    try:
        with open(file_path, 'r') as f:
            for line_num, raw_line in enumerate(f, start=1):
                line = raw_line.strip()

                # Ignore empty lines and comments
                if not line or line.startswith('#'):
                    continue

                # Must contain exactly one "="
                if line.count('=') != 1:
                    raise SyntaxError(
                        f"Ligne {line_num}: syntaxe invalide → '{raw_line.strip()}'"
                    )

                key, value = map(str.strip, line.split('='))

                # Empty key or value
                if not key or not value:
                    raise SyntaxError(
                        f"Ligne {line_num}: clé ou valeur manquante"
                    )

                # Unknown key
                if key not in required_keys:
                    raise KeyError(
                        f"Ligne {line_num}: clé inconnue '{key}'"
                    )

                # Duplicate key
                if key in config:
                    raise KeyError(
                        f"Ligne {line_num}: clé '{key}' déjà définie"
                    )

                # Type conversions

                if key in {'WIDTH', 'HEIGHT', 'SEED'}:
                    try:
                        value = int(value)
                    except ValueError:
                        raise ValueError(
                            f"Ligne {line_num}: {key} doit être un entier"
                        )

                    if value < 0:
                        raise ValueError(
                            f"Ligne {line_num}: {key} doit être positif"
                        )

                    if key in {'WIDTH', 'HEIGHT'} and not (3 <= value <= 100):
                        raise ValueError(
                            f"Ligne {line_num}: {key} doit être entre 3 et 100"
                        )

                elif key in {'ENTRY', 'EXIT'}:
                    parts = value.split(',')

                    if len(parts) != 2:
                        raise SyntaxError(
                            f"Ligne {line_num}: format invalide pour {key} (attendu x,y)"
                        )

                    try:
                        row, col = map(int, parts)
                    except ValueError:
                        raise ValueError(
                            f"Ligne {line_num}: coordonnées invalides pour {key}"
                        )

                    value = (row, col)

                elif key == 'PERFECT':
                    if value.lower() not in {'true', 'false'}:
                        raise ValueError(
                            f"Ligne {line_num}: PERFECT doit être True ou False"
                        )
                    value = value.lower() == 'true'
                
                elif key == 'ALGO':
                    value = value.upper()
                    if value not in {'DFS','PRIM'}:
                        raise ValueError(
                            f"Ligne {line_num}: ALGO doit être 'DFS' ou 'PRIM', valeur trouvée → '{value}'"
                        )
                config[key] = value

    except FileNotFoundError:
        raise FileNotFoundError(f"Fichier non trouvé: {file_path}")

    # Global validations


    # Check all required keys
    missing = required_keys - config.keys()
    if missing:
        raise KeyError(f"Clés manquantes: {', '.join(missing)}")

    width = config['WIDTH']
    height = config['HEIGHT']

    # Check ENTRY and EXIT inside bounds
    for point in ['ENTRY', 'EXIT']:
        row, col = config[point]
        if not (0 <= row < height and 0 <= col < width):
            raise ValueError(
                f"{point} ({row},{col}) est hors du labyrinthe "
                f"({height} lignes, {width} colonnes)"
            )

    # ENTRY and EXIT must be different
    if config['ENTRY'] == config['EXIT']:
        raise ValueError("ENTRY et EXIT ne peuvent pas être identiques")

    return config


# Test rapide
if __name__ == "__main__":
    try:
        cfg = read_config("config.txt")
        print("Configuration lue avec succès :")
        print(cfg)
    except Exception as e:
        print("Erreur de configuration :", e)