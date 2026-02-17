def read_config(file_path):
    config = {}
    valid_keys = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'PERFECT']

    try:
        with open(file_path, 'r') as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()

                # Ignorer commentaires et lignes vides
                if not line or line.startswith('#'):
                    continue

                if '=' not in line:
                    raise ValueError(f"Ligne {line_num}: format incorrect (pas de '='): {line}")

                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()

                if key not in valid_keys:
                    raise KeyError(f"Ligne {line_num}: clé inconnue '{key}'")

                # Conversion des types
                if key in ['WIDTH', 'HEIGHT']:
                    try:
                        config[key] = int(value)
                    except Exception:
                        raise ValueError(f"Ligne {line_num}: valeur de {key} doit être un entier: {value}")

                elif key in ['ENTRY', 'EXIT']:
                    try:
                        coords = tuple(map(int, value.split(',')))
                        if len(coords) != 2:
                            raise ValueError
                        config[key] = coords
                    except Exception:
                        raise ValueError(f"Ligne {line_num}: valeur de {key} doit être 'x,y': {value}")

                elif key == 'PERFECT':
                    if value.lower() not in ['true', 'false']:
                        raise ValueError(f"Ligne {line_num}: valeur de PERFECT doit être True ou False: {value}")
                    config[key] = value.lower() == 'true'

    except FileNotFoundError:
        raise FileNotFoundError(f"Fichier non trouvé: {file_path}")

    # Vérification que toutes les clés obligatoires sont présentes
    for k in valid_keys:
        if k not in config:
            raise KeyError(f"Clé obligatoire manquante dans le fichier: {k}")

    return config


# Test rapide
if __name__ == "__main__":
    try:
        cfg = read_config("file.txt")
        print("Configuration lue avec succès :")
        print(cfg)
    except Exception as e:
        print("Erreur de configuration :", e)