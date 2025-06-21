import requests

key = "cur_live_as4htvplWdJkeMLS6uT3ZObVELU7hmc75XIx5Mq6"
resp = requests.get(
  "https://api.currencyapi.com/v3/latest",
  headers={"apikey": key}
)
print(resp.status_code, resp.json())
