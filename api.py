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

# No Function for this yet, but maybe in the future

def update_balance(account_id, value, reason, username_creator):
    authorization_token = read_config_value("config.txt", "API_Token")
    headers = {"Authorization": f"Bearer {authorization_token}"}
    r = requests.post(
        
        f"{API_URL}/update_balance",
        json={"account_id": account_id, "value": value, "reason": reason, "amount_from": username_creator},
        headers=headers,
        timeout=5
    )
    r.raise_for_status()
    return r.json()

# calculate Food Price

def add_new_food(person_and_price_list):
    authorization_token = read_config_value("config.txt", "API_Token")
    headers = {"Authorization": f"Bearer {authorization_token}"}
    r = requests.post(
        f"{API_URL}/add_new_food",
        json=person_and_price_list,
        headers=headers,
        timeout=999
    )
    r.raise_for_status()
    return r.json()

# get Account data for specific account id

def get_account_data(userid):
    try:
        authorization_token = read_config_value("config.txt", "API_Token")
        headers = {"Authorization": f"Bearer {authorization_token}"}
        r = requests.post(f"{API_URL}/get_account_data", headers=headers, json={"id": userid}, timeout=5)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    #accounts = get_accounts()
    #print(accounts)
    #account_data = get_account_data(userid="example_user_id")
    #print(account_data)
    #response = update_balance(account_id=1, value=500)
    #print(response)

    add_new_food([{"name": "Test User", "price": 5.99}, {"name": "Test User 2", "price": 3.50}])
