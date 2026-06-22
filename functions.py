def read_config_value(filename, key):
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # leere Zeilen oder Kommentare überspringen
            if not line or line.startswith("#"):
                continue

            if line.startswith(key + "="):
                return line.split("=", 1)[1].strip()

    return None

def get_users():
    from api import get_accounts
    user_list = []
    accounts = get_accounts()
    for user in accounts["accounts"]:
        user_list.append(user[0])
        print(user)
    print(f"User List: {user_list}")
    return user_list

def Text_Only_Float_Validator():
    # Text only Float
    try:
        from PySide6.QtGui import QRegularExpressionValidator
        from PySide6.QtCore import QRegularExpression
        regex = QRegularExpression(r"^\d+([.,]\d+)?$")
        validator = QRegularExpressionValidator(regex)
        return validator
    except Exception as e:
        print(f"An error occurred while creating the validator: {e}")
        validator = None
    