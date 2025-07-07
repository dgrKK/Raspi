sudo apt update
sudo apt install python3-pip
pip3 install requests
import requests

url = "https://api.coindesk.com/v1/bpi/currentprice.json"

response = requests.get(url)
data = response.json()

btc_price = data["bpi"]["USD"]["rate"]
print(f"Current Bitcoin price in USD: {btc_price}")
