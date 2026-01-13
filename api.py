# api.py
import requests
from main import read_config_value
API_Server = read_config_value("config.txt", "API_Server")
API_PORT = read_config_value("config.txt", "API_Port")
API_URL = f"http://{API_Server}:{API_PORT}"

def get_accounts():
    authorization_token = read_config_value("config.txt", "API_Token")
    headers = {"Authorization": f"Bearer {authorization_token}"}

    r = requests.post(f"{API_URL}/accounts", headers=headers, timeout=5)
    r.raise_for_status()
    return r.json()

def update_balance(account_id, value):
    r = requests.post(
        f"{API_URL}/update",
        json={"id": account_id, "value": value},
        timeout=5
    )
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    accounts = get_accounts()
    print(accounts)
    #response = update_balance(account_id=1, value=500)
    #print(response)
